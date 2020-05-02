import subprocess

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output

def run():                                                      # Is Adb backup enabled for org apks, returns how many apks have adb backup enabled, and stores the list of adb enabled apps in "Adb Backup Enabled List(Org apks only).txt"
    ID = "F01"                                                       # ID should be always 3 chars to maintain table structure in console output
    Desc = "Internal Server Information exposed     "                # Desc should be less that 40 chars
    Status = "       "                                               # Status should be less than 7 Chars
    Comments = ""


    '''
    Code to check test case
    '''

    command="adb shell getprop ro.build.user"
    username=systemCmd(command)
    #print username

    command="adb shell getprop ro.build.host"
    hostname=systemCmd(command)
    #print hostname

    if "ch3uu" in hostname:
        Status = "FAILED "
    else:
        Status = "PASSED "

    Comments = "Found user : " + username.rstrip() + ", host : " + hostname.rstrip() + ". Do verify manually once"

    #print Comments

    return ID, Desc, Status, Comments

run()