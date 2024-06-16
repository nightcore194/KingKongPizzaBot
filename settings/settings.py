from pathlib import Path

ENCODING = "UTF-8"

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR.joinpath('settings/config/')
CONFIG_FILE = CONFIG_DIR.joinpath('config.json')

BOT_WEBHOOK = "PASTE YOUR URL HERE"