# this program is designed to manage soho networks that might be harder to keep track of. 
# its written in console to make it as lightweight as possible.
import os
import json

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

spacer = print("")

def mainMenu():
    cls()
    print("VRH81's IP Management Address Tool.")
    print("This tool is designed to store IP addresses for easier management.")
    spacer
    print("1 - List all networks")
    print("2 - Create a network")
    print("3 - Remove a network")
    print("4 - Add IP addresses")
    print("5 - Remove IP addresses")
    print("0 - Exit")
    spacer

    menuChoice = int(input())

    if menuChoice == 1:
        networkList()
    elif menuChoice == 2:
        networkCreate()
    elif menuChoice == 3:
        networkRemove() # TODO
    elif menuChoice == 4:
        ipAdd() # TODO
    elif menuChoice == 5:
        ipRemove() # TODO
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
        print("1 - Find by network name")
        print("2 - Find by network ID")

        netListChoice2 = int(input())
        if netListChoice2 == 1:
            cls()
            print("Type name of network: ")
            networkSearchName = input()
            #networksFile = open('networks.txt', 'r') # TODO
            networkList()
    elif netListChoice == 2:
        cls()
        networkFile = open('networks.txt','r')
        networkFileContent = networkFile.read()
        print(networkFileContent)
        spacer
        input()
        mainMenu()
    else:
        print("You need to type something that I can work with >:(")
        input()
        networkList()

def networkCreate():
    cls()
    print("Give your network a name:")
    networkCreateName = input()
    spacer
    print("Now type in the network ID in the format of X.X.X.X")
    networkCreateID = input()
    spacer
    networkFile = open('networks.txt','a+')
    networkFile.write("Name: " + networkCreateName + "\n")
    networkFile.write("ID: " + networkCreateID + "\n\n")
    networkFile.close()
    cls()
    print("Your network has been saved.")
    input()
    mainMenu()
        
#def networkRemove(): # TODO   

#def ipAdd(): # TODO

#def ipRemove():# TODO

mainMenu()