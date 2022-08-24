

"""
--------------------------------
Project: Eduroam Connect
Description: Eduroam Connect is a Python script that is used on Rasberry Pi. It configures the Raspberry Pi to be able
to establish a connection with a edoroam WiFi.
Files being changed:
  -  /etc/network/interfaces
  -  /etc/wpa_supplicant/wpa_supplicant.conf
  -  /etc/systemd/timesyncd.conf

Infos: Use DOMAIN and TIMESERVER to customize the script
Author: Pierre Antonschmids
--------------------------------
"""
import os
import sys
import errno

DOMAIN = "@hs-woe.de"
TIMESERVER = "time.jade-hs.de"

def main():
    username = ""
    password = ""
    if (IsSUDO()):
        if(AddOrRemoveEntry()):
            username = InputUser()
            password = InputPassword()
            CheckAddInterfaces()
            CheckAddWPA()
            ModifyWPAAuth(username,password) 
            CheckAddTimeServer()
            CheckForTTelesec()
            #AskForReboot()

        else:
            print("Remove Username/Password from wpa_supplicant.conf")
            ModifyWPAAuth("","")
            AskForReboot()
            
    else:
        sys.exit("You need root permissions to do this!\nPlease use 'sudo eduroamConnect.py'")


def IsSUDO():
    """
    Description: Try to create/remove a fooEdu folder in /etc to check if script is started with SUDO rights.
    Parameters: NONE
    Returns: BOOL 
    """
    try:
        if (os.path.exists('/etc/fooEdu')):
            os.rmdir('/etc/fooEdu')
        else:
            os.mkdir('/etc/fooEdu')
            os.rmdir('/etc/fooEdu')
        return True
    except IOError as e:
            if (e == errno.EACCES):
                return False


def AddOrRemoveEntry():
    """
    Description: A simple welcome text and question for the next step, a choice between Adding configuration to the system or removing Username/Password
    Parameters: NONE
    Returns: BOOL
    """
    answer = 0
    while (answer > 2 or answer < 1):
        print("Welcome to Eduroam Connect.\nThis Tool will help you configure this Raspberry Pi to be able to connect with your nearby eduroam WiFI")
        print("You need your eduroam logindata in order to successfully setup everything.\nExample:\nUsername:te9999@hs-woe.de\nPassword: Password")
        print("After Eduroam Connect was used, a reboot is nessesary for the configurations to be used\n")
        answer = int(input('\n1: Add configuration and set Username/Password\n2: Remove Username/Password\n')) 

        if(answer == 1):
            #Add
            return True
        if(answer == 2):
            #Remove
            return False



def InputUser():
    """
    Description: Allows the Input for a Username, and uses the DOMAIN to match it with the Username
    parameters: NONE
    return: STRING
    """
    isValid = False
    while (not isValid):
        username = input("Example:te9999"+DOMAIN+"\nUsername:")
        if HasRightDomain(username):
            isValid = True
        else:
            print("Not valid Username, please check example\n")
           
    return username

def InputPassword():
    """
    Description: Allows the Input for a password
    parameters: NONE
    return: STRING
    """
    password = input("Password:") 
    return password
    

def HasRightDomain(username):
    """
    Description: Checks if the domain matches the global DOMAIN variable
    Parameters: username - The username that needs to be checked
    Return: BOOL
    """
    if(DOMAIN in username):
        return True
    else:
        return False


def CheckAddInterfaces():
    """
    Description: Checks the /etc/network/interfaces, if it does not exist it creates one with the configuration of the entryString
    Parameters: NONE
    Return: NONE
    """

    filePath = "/etc/network/interfaces"
    entryString = "allow-hotplug wlan0\niface wlan0 inet manual\nwpa-conf /etc/wpa_supplicant/wpa_supplicant.conf\n"

    WriteIntoFile(filePath, entryString)


def CheckAddWPA():
    """
    Description: Checks the /etc/wpa_supplicant/wpa_supplicant.conf if it does not exist it creates one with the configuration of the entryString and entryString2
    Parameters: NONE
    Return: NONE
    """

    filePath = "/etc/wpa_supplicant/wpa_supplicant.conf"
    entryString = "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\ncountry=DE\n"
    entryString2 = "network={\n    ssid='eduroam'\n    proto=RSN\n    key_mgmt=WPA-EAP\n    eap=PEAP\n    identity=\n    password=\n    phase1='peaplabel=0'\n    phase2='auth=MSCHAPV2'\n}\n"
    checkWPAMapNetwork = {
        "network": [False, "network={\n"],
        "ssid": [False, "    ssid='eduroam'\n"],
        "proto": [False, "    proto=RSN\n"],
        "key_mgmt": [False, "    key_mgmt=WPA-EAP\n"],
        "eap": [False, "    eap=PEAP\n"],
        "identity": [False, "    identity="],
        "password": [False, "    password="],
        "phase1": [False, "    phase1='peaplabel=0'\n"],
        "phase2": [False, "    phase2='auth=MSCHAPV2'\n"]
    }

    checkTrue = 0
    checkCtrl = False

    if(os.path.exists(filePath)):
        with open(filePath, 'r') as file:
                if entryString in file.read():
                    checkCtrl = True
        with open(filePath, 'r') as file:
                allLines = file.readlines()
                #Check Lines and if True set key to True
                for line in allLines:
                        for key in checkWPAMapNetwork:
                            if checkWPAMapNetwork[key][1] in line:
                                checkWPAMapNetwork[key][0] = True
                                checkTrue +=1

    if (checkTrue == 9 and checkCtrl):
        print("WPA check successfull....")
    else:
        print("Missing entrys detected....")
        WriteIntoFile(filePath, entryString)
        WriteIntoFile(filePath, entryString2)     
             
          
def ModifyWPAAuth(username, password):
    """
    Description: Modifys the identity and password entry in the network block inside of the wpa_supplicant.conf
    Parameters: 
        username - The username for identity=
        password - The password for password=
    Return: NONE
    """

    #To make sure change is being done in network
    inNetwork = False
    filePath = "/etc/wpa_supplicant/wpa_supplicant.conf"
    if(os.path.exists(filePath)):
         with open(filePath, 'r+') as file:
            allLines = file.readlines()
            newLines = ""
            for line in allLines:
                #Makes sure ony entrys in network block are being changed
                if "network={" in line:
                    inNetwork = True
                    
                if "}" in line:
                    inNetwork = False

                if inNetwork and "identity=" in line:
                    line = "    identity='"+username+"'\n"

                if inNetwork and "password=" in line:
                    line = "    password='"+password+"'\n"

                newLines += line
            
            WriteIntoFile(filePath, newLines, True)
            print("Updating Username/Password for eduroam Login....")
    else:
        print(filePath+" not found, please use option 1")
                
def WriteIntoFile(filePath, entryString, overwrite=False):
    """
    Description: Is a function to write a string into a file.
    Parameters: 
        filePath - Example: "/etc/wpa_supplicant/wpa_supplicant.conf"
        entryString - Example: "Hello World"
        overwrite - OPTIONAL: complely overwrites the file.
    Return: NONE
    """   

    entryComment = "#-----Autogenerated with Eduroam Connect-----\n"
    output = "Added to {0}:\n{1}\n{2}\n---------------------\n" 
    if(overwrite):
         with open(filePath, 'w') as file:
            file.write(entryString)
    else:
        if(os.path.exists(filePath)):
            print(filePath+" found...")
            with open(filePath, 'r+') as file:
                if entryString not in file.read():
                    print("adding entry...")
                    file.write(entryComment+entryString)
                    print(output.format(filePath, entryComment, entryString))
        else:
            with open(filePath, 'a+') as file:
                    file.write(entryComment+entryString)
                    print(output.format(filePath, entryComment, entryString))

def CheckAddTimeServer():
    """
    Description: Checks the /etc/systemd/timesyncd.conf for the correct TIMESERVER entry and changes it when nessesary
    Parameters: NONE
    Return: NONE
    """ 

    entryString = "[TIME]\nNTP="+TIMESERVER+"\nRootDistanceMaxSec=5\n"
    filePath = "/etc/systemd/timesyncd.conf"
    if(os.path.exists(filePath)):
        with open(filePath, 'r') as file:
                allLines = file.readlines()
                newLines = ""
                #Check Lines and if True set key to True
                for line in allLines:
                    if "NTP=" in line:
                        line = "NTP="+TIMESERVER+"\n"
                    if "RootDistanceMaxSec" in line:
                        line = "RootDistanceMaxSec=5\n"
                    newLines += line
                WriteIntoFile(filePath, newLines, True)
                print("Timeserver set to: "+TIMESERVER+" ....")
    else:
        print("Cant find "+filePath+"....create file")
        WriteIntoFile(filePath, entryString, True)

def AskForReboot():
    """
    Description: Needs user confirmation for a reboot otherwise it will just close the script
    Parameters: NONE
    Return: NONE
    """  

    answer = 0
    while (answer > 2 or answer < 1):
        answer = int(input('Thanks for using Edoroam Connect\nA reboot is nesseary for the setting to be used.\n1: Reboot now!\n2: Not now!\n')) 
        if(answer == 1):
            #Yes
            os.system("reboot")
        if(answer == 2):
            #No
            sys.exit()

def CheckForTTelesec():
    filePath = "/etc/ssl/certs/T-TeleSec_GlobalRoot_Class_2.pem"
    certString = "-----BEGIN CERTIFICATE-----\nMIIDwzCCAqugAwIBAgIBATANBgkqhkiG9w0BAQsFADCBgjELMAkGA1UEBhMCREUx\nKzApBgNVBAoMIlQtU3lzdGVtcyBFbnRlcnByaXNlIFNlcnZpY2VzIEdtYkgxHzAd\nBgNVBAsMFlQtU3lzdGVtcyBUcnVzdCBDZW50ZXIxJTAjBgNVBAMMHFQtVGVsZVNl\nYyBHbG9iYWxSb290IENsYXNzIDIwHhcNMDgxMDAxMTA0MDE0WhcNMzMxMDAxMjM1\nOTU5WjCBgjELMAkGA1UEBhMCREUxKzApBgNVBAoMIlQtU3lzdGVtcyBFbnRlcnBy\naXNlIFNlcnZpY2VzIEdtYkgxHzAdBgNVBAsMFlQtU3lzdGVtcyBUcnVzdCBDZW50\nZXIxJTAjBgNVBAMMHFQtVGVsZVNlYyBHbG9iYWxSb290IENsYXNzIDIwggEiMA0G\nCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCqX9obX+hzkeXaXPSi5kfl82hVYAUd\nAqSzm1nzHoqvNK38DcLZSBnuaY/JIPwhqgcZ7bBcrGXHX+0CfHt8LRvWurmAwhiC\nFoT6ZrAIxlQjgeTNuUk/9k9uN0goOA/FvudocP05l03Sx5iRUKrERLMjfTlH6VJi\n1hKTXrcxlkIF+3anHqP1wvzpesVsqXFP6st4vGCvx9702cu+fjOlbpSD8DT6Iavq\njnKgP6TeMFvvhk1qlVtDRKgQFRzlAVfFmPHmBiiRqiDFt1MmUUOyCxGVWOHAD3bZ\nwI18gfNycJ5v/hqO2V81xrJvNHy+SE/iWjnX2J14np+GPgNeGYtEotXHAgMBAAGj\nQjBAMA8GA1UdEwEB/wQFMAMBAf8wDgYDVR0PAQH/BAQDAgEGMB0GA1UdDgQWBBS/\nWSA2AHmgoCJrjNXyYdK4LMuCSjANBgkqhkiG9w0BAQsFAAOCAQEAMQOiYQsfdOhy\nNsZt+U2e+iKo4YFWz827n+qrkRk4r6p8FU3ztqONpfSO9kSpp+ghla0+AGIWiPAC\nuvxhI+YzmzB6azZie60EI4RYZeLbK4rnJVM3YlNfvNoBYimipidx5joifsFvHZVw\nIEoHNN/q/xWA5brXethbdXwFeilHfkCoMRN3zUA7tFFHei4R40cR3p1m0IvVVGb6\ng1XqfMIpiRvpb7PO4gWEyS8+eIVibslfwXhjdFjASBgMmTnrpMwatXlajRWc2BQN\n9noHV8cigwUtPJslJj0Ys6lDfMjIq2SPDqO/nBudMNva0Bkuqjzx+zOAduTNrRlP\nBSeOE6Fuwg==\n-----END CERTIFICATE-----\n"

    if (not os.path.exists(filePath)):
        print("Missing certification detected: "+ filePath)
        with open(filePath, "a+") as file:
            file.write(certString)
        print("Created File: /etc/ssl/certs/T-TeleSec_GlobalRoot_Class_2.pem")
        RegisterCertification(certString)
    else:
        print(filePath+" found...")

def RegisterCertification(certString):
    filePath = "/etc/ssl/certs/ca-certifications.crt"

    WriteIntoFile(filePath, certString)



main()

