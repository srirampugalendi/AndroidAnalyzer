import subprocess
import tqdm
import time

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output

def run():
    ID = "A09"                                                       # ID should be always 3 chars to maintain table structure in console output
    Desc = "Debug Logs are enabled                  "                # Desc should be less that 40 chars
    Status = "       "                                               # Status should be less than 7 Chars
    Comments = ""

    cmd = "findstr /s /i Log.d( decompiledSource\*.* > Logs/DebugLog_find.txt"
    op = systemCmd(cmd)

    findDebugLog = "DebugLog_find.txt"
    uniqueName = None
    Count = 0
    with open(findDebugLog) as file:
        for line in file:
            appName = line.split('\\')
            #print line
            # if uniqueName == None:
            #     uniqueName = appName[1]
            #     print 'abc'
            #     print uniqueName
            #     continue
            if uniqueName != appName[1]:
                #print "123"

                uniqueName = appName[1]
                #print uniqueName
                Count += 1

    #print "[+] Total of " + str(Count) + " apks have debug logs enabled"
    if Count == 0:
        Status = "PASSED "
        Comments = "All Apks have debug logs disabled"

    else:
        Status = "FAILED "
        Comments = str(Count) + " Apks have debug logs enabled"


    return ID, Desc, Status, Comments

#run()