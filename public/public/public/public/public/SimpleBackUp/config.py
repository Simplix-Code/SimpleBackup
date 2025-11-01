import os
import json

DEFAULT_CONFIG_PATHS = [
    "/etc/SimpleBackUp/backup_config.json",
    "./backup_config.json",
]
DEFAULT_BACKUP_ROOT = "./backups"


def find_config_path_for_read():
    for path in DEFAULT_CONFIG_PATHS:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Keine backup_config.json gefunden.")


def find_config_path_for_write():
    for path in DEFAULT_CONFIG_PATHS:
        if os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            return path
    # fallback
    return "./backup_config.json"


def load_config():
    path = find_config_path_for_read()
    with open(path, "r") as f:
        return json.load(f), path


def save_config(cfg):
    path = find_config_path_for_write()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
    return path
