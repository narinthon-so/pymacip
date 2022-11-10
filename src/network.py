from getmac import get_mac_address
import re
import socket
from time import sleep
from libnmap.parser import NmapParser
from libnmap.process import NmapProcess
import logging as log
log.getLogger().setLevel(log.INFO)
from src.detectos import detectos


class Network:

    def getselfip(self) -> str:
        """get current Host IP address

        Returns:
            str: local IP address
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def getipbymac(self, mac: str) -> dict:
        """get local IP Address by MAC address 

        Args:
            mac (str): destination MAC address format: FF:FF:FF:FF:FF:FF

        Returns:
            dict: {status: bool, data: str}
        """
        # Validate mac address
        if self.is_valid_mac_address(mac) is False:
            log.error("Invalid mac address")
            return {"status": False, "data": "Invalid mac address"}
        # Nmap mac formats
        mac = self.__formatmac(mac)
        # Let try
        try:
            ip = self.getselfip()
            log.info(f'Input mac: {mac}, Local ip: {ip}')
            nm = NmapProcess(f'{ip}/24', options="-sP")
            # detect os
            if detectos() == "win32":
                nm.run_background()
            else:
                nm.sudo_run_background()
            # scan loop
            while nm.is_running():
                log.info("Nmap Scan running")
                sleep(2)
            nmap_report = NmapParser.parse(nm.stdout)
            res = next(filter(lambda n: n.mac == mac.strip().upper(), filter(
                lambda host: host.is_up(), nmap_report.hosts)), None)
            # Check result
            if res is None:
                log.info("Host is down or Mac address not exist")
                return {"status": False, "data": "Host is down or Mac address not exist"}
            else:
                log.info(f'\nMAC: {mac} with IP {res.address}')
                return {"status": True, "data": res.address}
        except Exception as e:
            log.error(e)
            return {"status": False, "data": "Host is down or Mac address not exist"}

    def is_valid_mac_address(self, mac: str) -> bool:
        # Function to validate MAC address.
        # Regex to check valid
        # MAC address
        regex = ("^([0-9A-Fa-f]{2}[:-])" +
                 "{5}([0-9A-Fa-f]{2})|" +
                 "([0-9a-fA-F]{4}\\." +
                 "[0-9a-fA-F]{4}\\." +
                 "[0-9a-fA-F]{4})$")

        # Compile the ReGex
        p = re.compile(regex)

        # If the string is empty
        # return false
        if (mac == None):
            return False

        # Return if the string
        # matched the ReGex
        if (re.search(p, mac)):
            return True
        else:
            return False

    def __formatmac(self, mac: str) -> str:
        if "-" in mac:
            return mac.replace("-", ":")
        else:
            return mac

    def getmacbyip(self, ip: str):
        """get MAC addresss by local IP Address

        Args:
            ip (str): local IP Address format: 192.168.20.17

        Returns:
            (str | None)
        """
        log.info(f'Input ip: {ip}')
        return get_mac_address(ip=ip)
