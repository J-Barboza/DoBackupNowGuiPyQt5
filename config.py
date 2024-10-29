import os
import json

def get_absolute_path(file_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

def load_config(config_file):
    config_path = get_absolute_path(config_file)
    if not os.path.exists(config_path):
        return None
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def save_config(config_file, config):
    config_path = get_absolute_path(config_file)
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)
