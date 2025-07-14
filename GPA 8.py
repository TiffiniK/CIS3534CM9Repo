#!/usr/bin/env python3
#networkFileRW.py
#Tiffin Kearney
#June 7, 2025

try:
    import json
except ImportError:
    print("Error: JSON module not found. Please install it.")
    exit()

ROUTERS_FILE = 'equip_r.txt'
SWITCHES_FILE = 'equip_s.txt'
UPDATED_FILE = 'updated.txt'
ERRORS_FILE = 'errors.txt'

UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device
        else:
            print("That device is not in the network inventory.")


def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        
        if len(octets) != 4:  
            invalidIPCount += 1
            invalidIPAddresses.append(ipAddress)
            print(SORRY)
            continue
        
        for byte in octets:
            try:
                byte = int(byte)
                if byte < 0 or byte > 255:
                    invalidIPCount += 1
                    invalidIPAddresses.append(ipAddress)
                    print(SORRY)
                    break
            except ValueError: 
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            
            return ipAddress, invalidIPCount         

def main():

    routers = {}
    switches = {}

    try:
        with open(ROUTERS_FILE, 'r') as r_file:
[cite_start]routers = json.load(r_file) [cite: 2]
    except FileNotFoundError:
        print(f"Error: {ROUTERS_FILE} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {ROUTERS_FILE}.")
        return

    try:
        with open(SWITCHES_FILE, 'r') as s_file:
    [cite_start]switches = json.load(s_file) [cite: 1]
    except FileNotFoundError:
        print(f"Error: {SWITCHES_FILE} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {SWITCHES_FILE}.")
        return

    updated = {}

    
    invalidIPAddresses = []


    devicesUpdatedCount = 0
    invalidIPCount = 0

    
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items():
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:

        
        device = getValidDevice(routers, switches)

        if device == 'x':
            quitNow = True
            break

        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)

                if 'r' in device:
            
            routers[device] = ipAddress
           

        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)
        
    
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    
    try:
        with open(UPDATED_FILE, 'w') as u_file:
            json.dump(updated, u_file, indent=4)
    except IOError:
        print(f"Error: Could not write to {UPDATED_FILE}.")


    print("Updated equipment written to file 'updated.txt'")
    print()
    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    
    try:
        with open(ERRORS_FILE, 'w') as e_file:
            for ip in invalidIPAddresses:
                e_file.write(ip + '\n')
    except IOError:
        print(f"Error: Could not write to {ERRORS_FILE}.")


    print("List of invalid addresses written to file 'errors.txt'")


if __name__ == "__main__":
    main()
