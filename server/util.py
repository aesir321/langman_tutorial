import os
import yaml


def get_config(env, config_resource):
    # Load config options for the given environment
    config_dict = yaml.load(config_resource, Loader=yaml.Loader)

    try:
        config_dict = config_dict[env]
    except KeyError:
        raise KeyError(
            f"Invalid ENV value '{env}' should be in {list(config_dict.keys)}, set using FLASK_ENV=value"
        )

    # Load any flask environment variables
    for key, value in os.environ.items():
        if key.startswith("FLASK_"):
            config_dict[key[6:]] = value
    # Load any env: values from the environment
    for key, value in config_dict.items():
        if isinstance(value, str) and value.startswith("env"):
            config_dict[key] = os.environ[value[4:]]
    # Put the values into the application config
    return config_dict
