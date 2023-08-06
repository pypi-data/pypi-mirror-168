import configparser
import sys

import schedulesy_qrcode.config as config


def main():
    if len(sys.argv) != 2:
        raise IndexError("Usage: qrcodes <path/to/config>")
    configuration = configparser.ConfigParser()
    configuration.read(sys.argv[1])
    config.ADE_CONF = configuration['ADE']
    config.S3_CONF = configuration['S3']
    config.QR_CONF = configuration['QRCode']
    config.FONT_CONF = configuration['Font']
    config.TEMPLATES_CONF = configuration['Template']

    from schedulesy_qrcode.refresh import refresh

    refresh()


if __name__ == '__main__':
    sys.exit(main())
