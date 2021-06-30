# this program is designed to manage soho networks that might be harder to keep track of. 
# its written in console to make it as lightweight as possible.
import os
import sqlite3

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

spacer = print("")

#pyMongoConnect = pymongo.MongoClient('mongodb://localhost:27017/')
#ipamDB = pyMongoConnect['IPAddressManagement'] # Database
#ipAddressTable = ipamDB['IP Address Table'] # Collection (table if you are mysql user)

def mainMenu():
    cls()
    print("VRH81's IP Management Address Tool.")
    print("This tool is designed to store IP addresses for easier management.")
    spacer
    print("1 - View networks")
    print("2 - Create a network")
    print("3 - Remove a network")
    print("0 - Exit")
    spacer

    menuChoice = int(input())

    if menuChoice == 1:
        networkList()
    elif menuChoice == 2:
        networkCreate()
    elif menuChoice == 3:
        networkRemove() # TODO
    elif menuChoice == 0:
        quit()
    else:
        print("You need to type something that I can work with >:(")
        input()
        mainMenu()


def networkList():
    cls()
    print("1 - Look for a specific network (UNAVAILABLE)") # TODO
    print("2 - View all networks")

    netListChoice = int(input())
    if netListChoice == 1:
        cls()
        dbcon = sqlite3.connect('networks.db')
        dbcur = dbcon.cursor()

        searchInput = input('Enter device name, interface, ip address or network ID: ')

        dbsearch = dbcon.execute("SELECT device,interface,ipaddr,netmask,netid FROM iptable WHERE device,interface,ipaddr,netmask,netid = VALUES (?);", (searchInput))
        networkList()
    elif netListChoice == 2:
        cls()
        dbcon = sqlite3.connect('networks.db')
        dbsearch = dbcon.execute("SELECT device,interface,ipaddr,netmask,netid FROM iptable")

        for row in dbsearch:
            print('Device = ' + row[0])
            print('Interface = ' + row[1])
            print('IP address = ' + row[2])
            print('Subnet mask = ' + row[3])
            print('Network ID = ' + row[4] + '\n')
        input()
        dbcon.close()
        mainMenu()
    else:
        print("You need to type something that I can work with >:(")
        input()
        networkList()

def networkCreate():
    cls()

    networkCreateDev = input("Enter device name: ")
    networkCreateInt = input("Enter interface: ")
    networkCreateIP = input("Enter IP address (x.x.x.x): ")
    networkCreateMask = input("Enter subnet mask (x.x.x.x): ")
    networkCreateID = input("Enter network ID (x.x.x.x): ")

    networkTable = {
        "device":networkCreateDev,
        "interface":networkCreateInt,
        "ipaddr":networkCreateIP,
        "subnetmask":networkCreateMask,
        "netid":networkCreateID
        }

    dbcon = sqlite3.connect('networks.db')
    dbcur = dbcon.cursor()

    dbcur.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='iptable' ''')

    if dbcur.fetchone()[0]==1:
        insertScript = "INSERT INTO iptable (device,interface,ipaddr,netmask,netid) VALUES (?,?,?,?,?);"
        dbcur.execute(insertScript,(networkCreateDev,networkCreateInt,networkCreateIP,networkCreateMask,networkCreateID))
        dbcon.commit()
        dbcon.close()

    else:
        dbcur.execute('''CREATE TABLE iptable (device,interface,ipaddr,netmask,netid)''')
        insertScript = "INSERT INTO iptable (device,interface,ipaddr,netmask,netid) VALUES (?,?,?,?,?);"
        dbcur.execute(insertScript,(networkCreateDev,networkCreateInt,networkCreateIP,networkCreateMask,networkCreateID))
        dbcon.commit()
        dbcon.close()

    cls()
    print('Device: ' + networkTable['device'])
    print('Interface: ' + networkTable['interface'])
    print('IP Address: ' + networkTable['ipaddr'])
    print('Subnet Mask: ' + networkTable['subnetmask'])
    print('Network ID: ' + networkTable['netid'] + '\n\n')
    input("Your network has been saved.")
    mainMenu()
        
#def networkRemove(): # TODO

mainMenu()