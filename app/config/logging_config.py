import yaml
import logging.config
import logging


def init_logger() -> dict:
    with open("logging_config.yml", "r") as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def get_module_logger():
    """
    Get a logger named after the module where this function is called.
    Automatically uses the calling module's __name__.
    """
    # Get the name of the module that called this function
    caller_name = logging.currentframe().f_back.f_globals["__name__"]
    return logging.getLogger(caller_name)
