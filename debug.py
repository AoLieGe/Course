import logging


def set_debug_level(param: str) -> None:
    """set logging debug level"""
    if param in ['1', 'true', 'True', 'y', 'Y']:
        logging.basicConfig(level=logging.DEBUG)
