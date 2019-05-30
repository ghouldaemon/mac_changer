#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():

    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-} You need to specify an interface, use --help for more information.")
    if not options.new_mac:
        parser.error("[-] You need to specify a new mac, use --help for more information")

    return options


def change_mac(interface, new_mac):

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

    print("[+] Your new MAC for interface " + interface + " is " + new_mac)


def get_current_mac(interface):

    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    mac_address_search_result = re.search(rb"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("Could not read Mac Address")


options = get_arguments()
current_mac = str(get_current_mac(options.interface))
print("Current MAC = " + current_mac)

change_mac(options.interface, options.new_mac)


