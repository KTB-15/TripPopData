import logging
from colorama import Fore, Style, init

init(autoreset=True)


class _CustomFormatter(logging.Formatter):
    FORMAT = {
        logging.DEBUG: Fore.BLUE + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.INFO: Fore.GREEN + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.ERROR: Fore.RED + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + Style.RESET_ALL,
    }

    def format(self, record):
        log_format = self.FORMAT.get(record.levelno)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


def get_logger(name: str = 'default') -> logging.Logger:
    # 로거 설정
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

    # 콘솔에 출력
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 스타일링
    ch.setFormatter(_CustomFormatter())

    logger.addHandler(ch)
    return logger


__all__ = ['get_logger']
