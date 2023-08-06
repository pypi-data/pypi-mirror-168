import configparser


def init_device_config(devices_file="./devices.ini") -> list:
    """
    Load device config

    Args:
        devices_file: devices_file config location

    Returns:
        list[str]: device configs.
    """
    new_device_config = configparser.ConfigParser()
    new_device_config.read(devices_file)
    return new_device_config


device_config = init_device_config()
