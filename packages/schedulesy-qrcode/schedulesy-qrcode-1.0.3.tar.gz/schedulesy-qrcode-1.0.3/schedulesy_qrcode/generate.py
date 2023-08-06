import io

import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

from schedulesy_qrcode.config import FONT_CONF, QR_CONF


def generate(rooms, color, client):
    def save_image(image, filename):
        output = io.BytesIO()
        image.save(output, "png")
        output.seek(0)
        client.upload(output, filename, "image/png")
        output.close()

    def single_room(room):
        print(f'🎨 Generating {".".join(room["path"])}.{room["name"]} ({room["id"]})')
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

        qr.add_data(f'{QR_CONF["url"]}/public/{room["id"]}')

        image = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=RadialGradiantColorMask(
                back_color=(255, 255, 255), center_color=color, edge_color=(0, 0, 0)
            ),
            embeded_image_path=QR_CONF['logo'],
        )

        header = QR_CONF['header']

        def split(a, n):
            k, m = divmod(len(a), n)
            return (
                a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)
            )

        footer = "\n".join(
            [" - ".join(x) for x in list(split(room["path"] + [room["name"]], 3))]
        )

        expanded_image = ImageOps.expand(image, border=20, fill="white")

        # Add define a new font to write in the border
        big_font = ImageFont.truetype(FONT_CONF['path'], int(FONT_CONF['header']))
        small_font = ImageFont.truetype(FONT_CONF['path'], int(FONT_CONF['footer']))

        # Instantiate draw object & add desired text
        draw_object = ImageDraw.Draw(expanded_image)
        draw_object.text(xy=(60, 10), text=header, fill=(0, 0, 0), font=big_font)

        draw_object.text(
            xy=(60, expanded_image.height - 55),
            text=footer,
            fill=(0, 0, 0),
            font=small_font,
        )

        bordered = ImageOps.expand(expanded_image, border=10, fill=tuple(color))

        # Preview the image
        # bordered.show()

        # Save the image
        # bordered.save(f'out/{room["id"]}.png')
        save_image(bordered, f'{room["id"]}.png')
        return bordered

    images = list(map(single_room, rooms))

    w, h = images[0].size

    separation = 2

    # create big empty image with place for images
    new_image = Image.new(
        "RGB", (w * 2 + separation, h * 2 + separation), color="white"
    )

    # put images on new_image
    new_image.paste(images[0], (0, 0))
    new_image.paste(images[1], (w + separation, 0))
    new_image.paste(images[2], (0, h + separation))
    new_image.paste(images[3], (w + separation, h + separation))

    s_ids = multi(rooms)
    # save it
    print(f"🎨 Generating {s_ids}")
    # new_image.save(f'out/{"-".join(s_ids)}.png')
    save_image(new_image, f"{s_ids}.png")


def multi(rooms):
    ids = [int(room["id"]) for room in rooms]
    ids.sort()
    return "-".join(list(map(str, ids)))
