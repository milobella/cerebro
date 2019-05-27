import configparser


def config_to_dict(config: configparser.ConfigParser):
    return {section: {key: config[section][key] for key in config[section]} for section in config.sections()}