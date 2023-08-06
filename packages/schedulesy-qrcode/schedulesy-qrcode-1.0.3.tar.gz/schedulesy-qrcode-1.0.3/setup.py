# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schedulesy_qrcode']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'boto3>=1.24.70,<2.0.0',
 'qrcode[pil]>=7.3.1,<8.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['qrcodes = schedulesy_qrcode.main:main']}

setup_kwargs = {
    'name': 'schedulesy-qrcode',
    'version': '1.0.3',
    'description': 'Schedulesy - Generates QRCodes for public schedules of classrooms',
    'long_description': "# Générateur de QRCodes pour Schedulesy\n\n## Installation des dépendances\n\n### `Poetry`\n\nL'outil utilise `poetry` comme gestionnaire de dépendances. Voir la [procédure d'installation](https://python-poetry.org/docs/master/#installation) (privilégier une version de `python` >= 3.9 pour l'installation de `poetry`).\n\n``` \npoetry install\n```\n\n### `Pip`\n\nUne alternative est d'utiliser `pip` pour les dépendances. Des fichiers sont fournis pour les différents environnements.\n\nPour installer et exécuter :\n\n```\npip install -r requirements/common.txt\n```\n\nPour installer aussi les dépendances de développement : \n\n```\npip install -r requirements/dev.txt\n```\n\n## Usage\n\nVous devez créer un fichier de configuration en vous inspirant du fichier `config.ini.sample`.\n\n``` \npython main.py config.ini\n🔗 Connecting to ADE\n📖 Setting project\n💾 Fetching data\n🪣 Bucket example already exists\n⬇️ Downloading flat.json\n⬆️ Uploading file tree.json\n⬆️ Uploading file flat.json\n⬆️ Uploading file index.html\n```",
    'author': 'DIP - Université de Strasbourg',
    'author_email': 'dnum-dip@unistra.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
