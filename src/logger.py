import logging


def setup_logger(name: str, log_file: str) -> logging.Logger:
    """Логер, который записывает результат работы функции в файл"""
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(log_file, "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger
