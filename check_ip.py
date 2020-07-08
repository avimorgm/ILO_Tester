import sys
import redfish
from redfish.rest.v1 import ServerDownOrUnreachableError
import os

def main():
    with open("/Users/avimor/Downloads/ceph-ansible-rhcs-4-vagrant3/serverlist.txt", "r") as f:
        lines = f.read().splitlines()
        for host in lines:
            try:
                ilo_url = host
                SYSTEM_URL = ilo_url
                LOGIN_ACCOUNT = "admin"
                LOGIN_PASSWORD = "password"
                print(SYSTEM_URL)
                redfish_obj = redfish.redfish_client(base_url=SYSTEM_URL, username=LOGIN_ACCOUNT,
                                                     password=LOGIN_PASSWORD)
                redfish_obj.login()
                connection(redfish_obj,ilo_url)
            except ServerDownOrUnreachableError as e:
                sys.stderr.write("ERROR: server not reachable or does not support RedFish.\n")
                sys.exit()


def connection(redfish_obj,ilo_url):
    class Servers:

        def __init__(self, url):
            self.url = url

        def server_list(self):
            RESPONSE = redfish_obj.get(self.url)
            serial = (RESPONSE.dict)['SerialNumber']
            ipaddr = ilo_url
            ipaddr.split('//')
            ipaddrs = ipaddr.split('//')[1]
            hostname = (RESPONSE.dict)['HostName']
            print ("Collect Hostname and Serial server of:" + ' ' + str(ipaddrs))

            with open('/Users/avimor/Downloads/ceph-ansible-rhcs-4-vagrant3/result_file.txt', "a") as out:
                out.write('{}  {}  {}'.format('The Server Serial number is:' + ' ' + serial +',', 'The ILO IP ADDR is:' + ' '+  ipaddrs +',', 'The HostName Is:' + ' ' + hostname +'.' + os.linesep))


    p1 = Servers('/redfish/v1/Systems/1/')
    p1.server_list()


if __name__ == "__main__":
    main()
