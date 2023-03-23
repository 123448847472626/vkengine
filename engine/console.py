import logging

file_log = logging.FileHandler('logs.txt')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out),
                    format='[%(asctime)s | %(levelname)s] [VkEngine] %(message)s',
                    datefmt='%d.%m.%Y %H:%M:%S',
                    level=logging.INFO)


async def log(text):
    logging.info(text)


async def error(text):
    logging.error(text)


async def warning(text):
    logging.warning(text)