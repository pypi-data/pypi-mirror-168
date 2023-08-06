# Générateur de QRCodes pour Schedulesy

## Installation des dépendances

### `Poetry`

L'outil utilise `poetry` comme gestionnaire de dépendances. Voir la [procédure d'installation](https://python-poetry.org/docs/master/#installation) (privilégier une version de `python` >= 3.9 pour l'installation de `poetry`).

``` 
poetry install
```

### `Pip`

Une alternative est d'utiliser `pip` pour les dépendances. Des fichiers sont fournis pour les différents environnements.

Pour installer et exécuter :

```
pip install -r requirements/common.txt
```

Pour installer aussi les dépendances de développement : 

```
pip install -r requirements/dev.txt
```

## Usage

Vous devez créer un fichier de configuration en vous inspirant du fichier `config.ini.sample`.

``` 
python main.py config.ini
🔗 Connecting to ADE
📖 Setting project
💾 Fetching data
🪣 Bucket example already exists
⬇️ Downloading flat.json
⬆️ Uploading file tree.json
⬆️ Uploading file flat.json
⬆️ Uploading file index.html
```