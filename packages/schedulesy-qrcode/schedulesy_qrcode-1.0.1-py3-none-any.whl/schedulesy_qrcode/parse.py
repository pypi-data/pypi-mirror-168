import collections
import json
import random
import uuid
import xml.etree.ElementTree as ET
from functools import lru_cache
from io import BytesIO, StringIO

import schedulesy_qrcode.generate
from schedulesy_qrcode.generate import multi
from schedulesy_qrcode.render import render


class ADE_Parser:

    FLAT = "flat.json"
    tree = {}

    def __init__(self, client):
        self.s3_client = client
        self.flat = (
            {"rooms": {}, "paths": {}}
            if not self.s3_client.exists(ADE_Parser.FLAT)
            else json.loads(self.s3_client.get(ADE_Parser.FLAT))
        )

    def hash_room(self, room):
        content = room["path"].copy()
        content.append(room["name"])
        content.append(",".join(list(map(str, room["color"]))))
        return self.hash_path(content)

    def hash_path(self, path):
        return self._hash("%%".join(path))

    @lru_cache(maxsize=1000)
    def _hash(self, path):
        return str(uuid.uuid3(uuid.NAMESPACE_DNS, path))

    def random_color(self):
        color = [random.randint(0, 255) for _ in range(3)]
        color[random.randint(0, 2)] = 0
        return color

    def dig(self, path, element, center_color, branch):
        rooms = []

        def compare(room_list, building_color):
            final_color = building_color
            if len(room_list) == 4:
                changed = False
                branch[f"Planche {multi(rooms)}"] = {}
                for room in room_list:
                    if self.hash_path(room["path"]) in self.flat["paths"]:
                        final_color = self.flat["paths"][self.hash_path(room["path"])]
                        room["color"] = final_color
                    if room["id"] in self.flat["rooms"]:
                        changed |= room["id"] not in self.flat["rooms"] or self.flat[
                            "rooms"
                        ][room["id"]] != self.hash_room(room)
                    else:
                        changed = True
                    branch[f"Planche {multi(rooms)}"][room['name']] = room
                if changed:
                    for room in room_list:
                        self.flat["rooms"][room["id"]] = self.hash_room(room)
                        self.flat["paths"][self.hash_path(room["path"])] = final_color
                    schedulesy_qrcode.generate.generate(
                        room_list, final_color, self.s3_client
                    )
                    self.save_progress()
                room_list = []
            return room_list

        for child in element:
            if child.tag == "leaf":
                rooms.append(
                    {
                        "id": child.attrib["id"],
                        "path": path,
                        "name": child.attrib["name"],
                        "color": center_color,
                    }
                )
                rooms = compare(rooms, center_color)
            if child.tag == "branch":
                branch[child.attrib["name"]] = {}
                sub_d = branch[child.attrib["name"]]
                new_path = path.copy()
                new_path.append(child.attrib["name"])
                color = self.random_color()
                self.dig(new_path, child, color, sub_d)
        if len(rooms) > 0:
            # print("Duplicating rooms")
            while len(rooms) < 4:
                rooms.append(rooms[0])
            rooms = compare(rooms, center_color)

    def save_progress(self):
        self.s3_client.upload(
            BytesIO(json.dumps(self.tree).encode("UTF-8")),
            "tree.json",
            "application/json",
        )
        self.s3_client.upload(
            BytesIO(json.dumps(self.flat).encode("UTF-8")),
            ADE_Parser.FLAT,
            "application/json",
        )
        # open("out.json", "w").write(json.dumps(self.tree))
        # open("flat.json", "w").write(json.dumps(self.flat))

    def parse(self, content):
        classrooms = ET.fromstring(content)[0]
        self.dig([], classrooms, self.random_color(), self.tree)

        self.save_progress()
        ordered_tree = json.loads(json.dumps(self.tree, sort_keys=True))
        # open("ordered_tree.json", "w").write(json.dumps(ordered_tree))
        self.s3_client.upload(
            BytesIO(render(ordered_tree).encode("UTF-8")), "index.html", "text/html"
        )
        open("index.html", "w").write(render(ordered_tree))
