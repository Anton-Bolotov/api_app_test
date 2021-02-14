from configparser import ConfigParser


def config(file_name='settings.ini', section='postgresql'):
    cfg = ConfigParser()
    cfg.read(file_name)
    items = cfg.items(section)
    settings_dict = {}

    for item in items:
        settings_dict[item[0]] = item[1]

    return settings_dict
