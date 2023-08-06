import json

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

from schedulesy_qrcode.config import S3_CONF, TEMPLATES_CONF


def render(data):
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_CONF['path']), autoescape=select_autoescape()
    )
    template = env.get_template("tree.html")

    return template.render(
        data=data,
        s3={
            "endpoint": S3_CONF['endpoint'],
            "bucket": S3_CONF['bucket'],
            "tenant": S3_CONF['tenant'],
        },
    )


# data = json.load(open('out.json'))
# print(render(data))
