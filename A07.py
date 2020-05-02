import subprocess

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output

def run(scope):                                                      # Is Adb backup enabled for org apks, returns how many apks have adb backup enabled, and stores the list of adb enabled apps in "Adb Backup Enabled List(Org apks only).txt"
    ID = "A07"                                                       # ID should be always 3 chars to maintain table structure in console output
    Desc = "ADB backup enabled                      "                # Desc should be less that 40 chars
    Status = "       "                                               # Status should be less than 7 Chars
    Comments = ""


    '''
    Code to check test case
    '''

    systemCmd('adb shell pm list packages > packagesList.txt')

    fileName = scope
    fd_OrgApks = open("Logs/Adb_Backup_Enabled_List.txt", "wb")
    appCount = 0
    with open(fileName) as file:
        for line in file:

                    var1 = systemCmd('adb shell dumpsys package ' + line.rstrip() + ' | find "ALLOW_BACKUP"')

                    if var1:
                        #print packageName
                        fd_OrgApks.write(line.rstrip() + "\n")
                        appCount = appCount + 1

    #print appCount
    fd_OrgApks.close()
    if appCount > 0:
        Status = "FAILED "
    else:
        Status = "PASSED "

    Comments = str(appCount) + " Org APKs with ADB Backup enabled found. More info in Logs"

    #printTestResults(ID, Desc, Status, Comments)
    return ID, Desc, Status, Comments
    #print  ID, Desc, Status, Comments

#run("nonDeviceApks.txt")