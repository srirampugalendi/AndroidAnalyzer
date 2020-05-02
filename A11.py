import subprocess
import tqdm
import time
from xml.dom import minidom
import os.path

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output


def run():

    # As of API level 23, the following permissions are classified as Dangerous Permissions:

    dangerousPermissions = [
        'READ_CALENDAR',
        'WRITE_CALENDAR',
        'CAMERA',
        'READ_CONTACTS',
        'WRITE_CONTACTS',
        'GET_ACCOUNTS',
        'ACCESS_FINE_LOCATION',
        'ACCESS_COARSE_LOCATION',
        'RECORD_AUDIO',
        'READ_PHONE_STATE',
        'READ_PHONE_NUMBERS',
        'CALL_PHONE',
        'ANSWER_PHONE_CALLS',
        'READ_CALL_LOG',
        'WRITE_CALL_LOG',
        'ADD_VOICEMAIL',
        'USE_SIP',
        'PROCESS_OUTGOING_CALLS',
        'BODY_SENSORS',
        'SEND_SMS',
        'RECEIVE_SMS',
        'READ_SMS',
        'RECEIVE_WAP_PUSH',
        'RECEIVE_MMS',
        'READ_EXTERNAL_STORAGE',
        'WRITE_EXTERNAL_STORAGE',
        'INSTALL_PACKAGES',
    ];

    ID = "A11"                                         # ID should be always 3 chars to maintain table structure in console output
    Desc = "Applications with dangerous permissions "  # Desc should be less that 40 chars
    Status = "       "                                 # Status should be less than 7 Chars
    Comments = ""

    logfile = open("Logs/dangerousPermissions.txt", "wb")

    op = systemCmd("dir /b disassembledSource")
    appFolders = op.split('\r\n')
    #print appFolders
    appcount = 0
    for folder in appFolders:
        tmpFolder = None
        #print folder
        logfile.write("\n\n"+folder+"\n\n")
        filePath = "\"disassembledSource/" + str(folder) + "/AndroidManifest.xml\""
        #print os.path.isfile(filePath)
        if os.path.isfile(filePath) is False:
            continue
        #filePath = "disassembledSource/AutoInstall/AndroidManifest.xml"
        #print filePath
        xmldoc = minidom.parse(filePath)
        itemlist = xmldoc.getElementsByTagName('uses-permission')
        #print itemlist
        #print(len(itemlist))
        if len(itemlist) > 0:
            # print(itemlist[0].attributes['android:name'].value)
            for s in itemlist:
                #print s
                for d in dangerousPermissions:
                    #print d
                    if str(d) in s.attributes['android:name'].value:
                        #print(s.attributes['android:name'].value)
                        logfile.write(s.attributes['android:name'].value+"\n")
                        # algo to calc app count
                        if tmpFolder != folder:
                            appcount += 1
                        tmpFolder = folder
    logfile.close()
    if appcount > 0:
        Status = "  NR   "  # Status should be less than 7 Chars
        Comments = str(appcount) + " Apks requests dangerous permissions. Check Logs/dangerousPermissions.txt"
    else:
        Status = "PASSED "  # Status should be less than 7 Chars
        Comments = "No Apks with dangerous permissions found"

    return ID, Desc, Status, Comments

#run()