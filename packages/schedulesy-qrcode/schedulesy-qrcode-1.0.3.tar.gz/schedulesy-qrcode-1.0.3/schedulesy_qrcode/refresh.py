import xml.etree.ElementTree as ET

import requests

from schedulesy_qrcode.ceph import S3_client
from schedulesy_qrcode.config import ADE_CONF
from schedulesy_qrcode.parse import ADE_Parser

BASE_URL = ADE_CONF['url']


def refresh():
    print("🔗 Connecting to ADE")
    response = requests.get(
        BASE_URL,
        params={
            "login": ADE_CONF['user'],
            "password": ADE_CONF['password'],
            "function": "connect",
        },
    )
    session_id = ET.fromstring(response.text).attrib["id"]
    print("📖 Setting project")
    requests.get(
        BASE_URL,
        params={
            "sessionId": session_id,
            "function": "setProject",
            "projectId": ADE_CONF['project_id'],
        },
    )
    print("💾 Fetching data")
    response = requests.get(
        BASE_URL,
        params={
            "sessionId": session_id,
            "function": "getResources",
            "tree": "true",
            "category": "classroom",
            "detail": "0",
        },
    )

    parser = ADE_Parser(S3_client())
    # open('ade.xml','w').write(response.text)
    parser.parse(response.text)
