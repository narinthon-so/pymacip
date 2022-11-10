import sys
import logging as log
log.getLogger().setLevel(log.INFO)


def detectos() -> str:
    log.info(f'sys.platform = {sys.platform}')
    if sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('darwin'):
        return 'darwin'
    elif sys.platform.startswith('win32'):
        return 'win32'
