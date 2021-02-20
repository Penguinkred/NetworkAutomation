#!/usr/bin/env python

# import modules netmiko for connection, regex for ip checking, and getpass for passwords.
import netmiko
import re
from getpass import getpass

# Regex IP compare data
regex = "^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"


# Check if ip is valid. loop if not.
def check(address):
    if re.search(regex, address):
        return True
    else:
        print("Invalid Ip address")
        return False


print("Make an ssh connection to the cisco device")
address = input("ip of device:")
while not check(address):
    address = input("ip of device:")

# Make connection to the cisco device
router = dict(
    host=address,
    port=8181,
    device_type="cisco_ios",
    username=input("Username: "),
    password=getpass("Password: ")
)

# User input for Basic config setup
IntLo = input("Enter loopback interface number:")
DescLo = input("Enter description for loopback:")
IpLo = input("Enter ip for loopback:")
MaskLo = input('Enter netmask for loopback:')

loopback = {"int_name": "loopback{}".format(IntLo),
            "description": DescLo,
            "ip": IpLo,
            "netmask": MaskLo}

interface_config = [
    "interface {}".format(loopback["int_name"]),
    "description {}".format(loopback["description"]),
    "ip address {} {}".format(loopback["ip"], loopback["netmask"]),
    "no shutdown"
]

print("Attempting to connect...")
conn = netmiko.Netmiko(**router)
print("-"*30 + "\nConnection to router has been made!\n" + "-"*30)
output = conn.send_config_set(interface_config)
print(output)
print("backing up running config")
backupconfig = conn.send_config_set('do show run')
CONFIG_FILE = open("BackupConfig.txt", "a")
CONFIG_FILE.write(backupconfig)
CONFIG_FILE.close()
print('file saved to running directory')
conn.disconnect()
