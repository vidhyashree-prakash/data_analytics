import logging

def setup_logger(logger_name,level=logging.DEBUG,fileName="server.log"):
    # Create a custom logger
    logger = logging.getLogger(logger_name)

    # Configure the custom logger
    logger.setLevel(level)
    file_handler = logging.FileHandler(fileName)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger