# this program is designed to manage soho networks that might be harder to keep track of. 
# its written in console to make it as lightweight as possible.
import os
import sqlite3
from sqlite3.dbapi2 import Cursor

# console clear function
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

spacer = print("")

# this function represents the base of the program
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

    menuChoice = int(input()) # input is parsed to an integer

    if menuChoice == 1:
        networkList()
    elif menuChoice == 2:
        networkCreate()
    elif menuChoice == 3:
        networkRemove() 
    elif menuChoice == 0:
        quit()
    else:
        print("You need to type something that I can work with >:(")
        input()
        mainMenu()

# search function for the database
def networkList():
    cls()
    print("1 - Search by IP address")
    print("2 - View all networks")
    print('0 - Return')

    netListChoice = int(input())
    if netListChoice == 1:
        cls()
        dbcon = sqlite3.connect('networks.db') # connects to the database
        dbcur = dbcon.cursor()

        searchInput = input('Enter IP address [x.x.x.x]')

        dbsearch = '''SELECT * FROM iptable WHERE ipaddr=?;''' # queries the database for the users search
        dbcur.execute(dbsearch,(searchInput,)) 
        entries = dbcur.fetchall()
        for row in entries:
            print('Device = ' + row[0])
            print('Interface = ' + row[1])
            print('IP address = ' + row[2])
            print('Subnet mask = ' + row[3])
            print('Network ID = ' + row[4] + '\n')
        dbcur.close()
        # and then prints them very nicely
        input()
        mainMenu()
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
    elif netListChoice == 0:
        mainMenu()
    else:
        print("You need to type something that I can work with >:(")
        input()
        networkList()

def networkCreate():
    cls()

    networkCreateDev = input("Enter device name: ")
    networkCreateInt = input("Enter interface: ")
    networkCreateIP = input("Enter IP address [x.x.x.x]: ")
    networkCreateMask = input("Enter subnet mask [x.x.x.x]: ")
    networkCreateID = input("Enter network ID [x.x.x.x]: ")

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

    if dbcur.fetchone()[0]==1: # checks to see if the table exists in the database
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
        
def networkRemove(): # TODO
    print("1 - Delete by IP Address")
    print("2 - Delete all entries")

    choice = int(input())
    dbcon = sqlite3.connect('networks.db')
    dbcur = dbcon.cursor()

    if choice == 1:
        cls()

        searchInput = input('Enter IP address [x.x.x.x]: ')

        dbsearch = '''SELECT * FROM iptable WHERE ipaddr=?;'''
        dbcur.execute(dbsearch,(searchInput,))
        entries = dbcur.fetchall()
        for row in entries:
            print('Device = ' + row[0])
            print('Interface = ' + row[1])
            print('IP address = ' + row[2])
            print('Subnet mask = ' + row[3])
            print('Network ID = ' + row[4] + '\n')
        dbcur.close()

        choice2 = input('Are you sure you wish to delete this entry?[y/n]: ')
        
        if choice2 == 'y':     
            deleteSqliteRecord(searchInput)
            print('Entry deleted.')
            input()
            mainMenu()
        elif choice2 == 'n':
            mainMenu()
        else:
            print("You need to type something that I can work with >:(")
            input()
            networkRemove()
    elif choice == 2:
        
        choice2 = input('Are you sure you wish to delete all entries? !THIS CAN NOT BE UNDONE! [y/n]: ')
        
        if choice2 == 'y':     
            dbcur.execute("DROP TABLE iptable")
            print('Entry deleted.')
            input()
            mainMenu()
        elif choice2 == 'n':
            mainMenu()
        else:
            print("You need to type something that I can work with >:(")
            input()
            networkRemove()

# function to delete entries
def deleteSqliteRecord(ipaddr):
    try:
        dbcon = sqlite3.connect('networks.db')
        dbcur = dbcon.cursor()

        dbdelete = """DELETE from iptable where ipaddr = ?"""
        dbcur.execute(dbdelete, (ipaddr,))
        dbcon.commit()
        dbcur.close()

    except sqlite3.Error as error:
        print("Failed to delete reocord from a sqlite table", error)
    finally:
        if dbcon:
            dbcon.close()
            mainMenu()

mainMenu()

