import sys
import redfish
from redfish.rest.v1 import ServerDownOrUnreachableError

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
                 redfish_obj = redfish.redfish_client(base_url=SYSTEM_URL, username=LOGIN_ACCOUNT, password=LOGIN_PASSWORD)
                 redfish_obj.login()
                 connection(redfish_obj)
            except ServerDownOrUnreachableError as e:
                 sys.stderr.write("ERROR: server not reachable or does not support RedFish.\n")
                 sys.exit()

def connection(redfish_obj):

    class Servers:

        def __init__(self, url, val, var):
            self.url = url
            self.val = val
            self.var = var

        def server_check(self):

            if self.val == 'PowerSuppliesMismatch':
                RESPONSE = redfish_obj.get(self.url)
                self.val = (RESPONSE.dict)['Oem']['Hpe']['AggregateHealthStatus']['PowerSupplies'][self.val]
                print("The status of the" + ' ' + self.var + ' ' + str(self.val))
                if self.val == 'False':
                    print ("All OK")
                else:
                    print ("Error in the" + self.var)
                    print ("Generating some enformation")
                    serial = (RESPONSE.dict)['SerialNumber']
                    print ("The serial number is:" + ' ' + str(serial))
                    hostname = (RESPONSE.dict)['HostName']
                    print ("The hostname is:" + ' ' + str(hostname))
                    with open('/Users/avimor/Downloads/ceph-ansible-rhcs-4-vagrant3/' + hostname + '.txt', "w") as out:
                        out.write('{}\n{}\n'.format(serial, hostname))

            elif self.val == 'FanRedundancy':
                RESPONSE = redfish_obj.get(self.url)
                self.val = (RESPONSE.dict)['Oem']['Hpe']['AggregateHealthStatus'][self.val]
                print("The status of the" + ' ' + self.var + ' ' + str(self.val))
                if self.val == 'Redundant':
                    print ("All OK")
                else:
                    print ("Error in the" + self.var)
                    print ("Generating some enformation")
                    serial = (RESPONSE.dict)['SerialNumber']
                    print ("The serial number is:" + ' ' + str(serial))
                    hostname = (RESPONSE.dict)['HostName']
                    print ("The hostname is:" + ' ' + str(hostname))
                    with open('/Users/avimor/Downloads/ceph-ansible-rhcs-4-vagrant3/' + hostname + '.txt', "w") as out:
                        out.write('{}\n{}\n'.format(serial, hostname))

            else:
                RESPONSE = redfish_obj.get(self.url)
                self.val = (RESPONSE.dict)['Oem']['Hpe']['AggregateHealthStatus'][self.val]['Status']['Health']
                print("The status of the" + ' ' + self.var + ' ' + str(self.val))
                if self.val == 'OK':
                    print ("All OK")
                else:
                    print ("Error in the" + self.var)
                    print ("Generating some enformation")
                    serial = (RESPONSE.dict)['SerialNumber']
                    print ("The serial number is:" + ' ' + str(serial))
                    hostname = (RESPONSE.dict)['HostName']
                    print ("The hostname is:" + ' ' + str(hostname))
                    with open('/Users/avimor/Downloads/ceph-ansible-rhcs-4-vagrant3/' + hostname + '.txt', "w") as out:
                        out.write('{}\n{}\n'.format(serial, hostname))


    p1 = Servers('/redfish/v1/Systems/1/', 'SmartStorageBattery', 'SmartStorageBattery_R')  # type: Person
    p1.server_check()

    p2 = Servers('/redfish/v1/Systems/1/', 'Network', 'Network_R')
    p2.server_check()

    p3 = Servers('/redfish/v1/Systems/1/', 'PowerSupplies', 'PowerSupplies_R')
    p3.server_check()

    p4 = Servers('/redfish/v1/Systems/1/', 'Storage', 'Storage_R')
    p4.server_check()

    p5 = Servers('/redfish/v1/Systems/1/', 'Temperatures', 'Temperatures_R')
    p5.server_check()

    p6 = Servers('/redfish/v1/Systems/1/', 'Processors', 'Processors_R')
    p6.server_check()

    p7 = Servers('/redfish/v1/Systems/1/', 'BiosOrHardwareHealth', 'BiosOrHardwareHealth_R')
    p7.server_check()

    p8 = Servers('/redfish/v1/Systems/1/', 'Memory', 'Memory_R')
    p8.server_check()

    p9 = Servers('/redfish/v1/Systems/1/', 'Fans', 'Fans_R')
    p9.server_check()

    p10 = Servers('/redfish/v1/Systems/1/', 'FanRedundancy', 'FanRedundancy_R')
    p10.server_check()

    p10 = Servers('/redfish/v1/Systems/1/', 'PowerSuppliesMismatch', 'PowerSuppliesMismatch_R')
    p10.server_check()

if __name__ == "__main__":
    main()

#REDFISH_OBJ.logout()
