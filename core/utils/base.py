import os


class ConfigException(Exception):
    pass


def get_settings_path(base_dir, list_name: tuple):
    for list_name in list_name:
        if os.path.exists(os.path.join(base_dir, list_name)):
            return os.path.join(base_dir, list_name)
    raise ConfigException('Config file not found')


