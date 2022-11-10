from src.network import Network
from time import sleep
import logging as log
log.getLogger().setLevel(log.INFO)


def main():
    net = Network()

    # get local ip by mac
    # Good case
    log.info(net.getipbymac("18-c0-4d-7c-56-82"))
    sleep(1)
    log.info(net.getipbymac("b8-ca-3a-80-f9-33"))
    sleep(1)
    log.info(net.getipbymac("74:d4:35:64:23:46"))
    sleep(1)
    log.info(net.getipbymac("c4:4f:33:e2:b8:84"))
    sleep(1)
    # Bad case
    log.info(net.getipbymac("18c0-4d-7c-56-82"))
    sleep(1)
    log.info(net.getipbymac("b8-ca-3a-80-f9-3X"))
    sleep(1)
    log.info(net.getipbymac("-64-23-46"))
    sleep(1)
    log.info(net.getipbymac("c4-4f-33-e2-b8-88"))  # mac not exist

    # get mac by ip
    # Good case
    log.info(net.getmacbyip("192.168.20.17"))
    sleep(1)
    log.info(net.getmacbyip("192.168.20.113"))
    sleep(1)
    # Bad case
    log.info(net.getmacbyip("192.168.20."))
    sleep(1)
    log.info(net.getmacbyip("192.168.xx.113"))
    sleep(1)


if __name__ == "__main__":
    main()
