import subprocess

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output

def run():

    ID = "A01"                                         # ID should be always 3 chars to maintain table structure in console output
    Desc = "Hardcoded Keys in Apk file              "  # Desc should be less that 40 chars
    Status = "       "                                 # Status should be less than 7 Chars
    Comments = ""

    cmd = 'findstr /s /i "secretkey" decompiledSource\*.* > Logs/Keys_1.txt'
    op = systemCmd(cmd)
    cmd = 'findstr /s /i "secretkey123" decompiledSource\*.* > Logs/Keys_2.txt'
    op = systemCmd(cmd)



    findDebugLog = "Logs/Keys_1.txt"
    uniqueName = None
    Count = 0
    with open(findDebugLog) as file:
        for line in file:
            appName = line.split(':')

            if uniqueName != appName[0]:
                # print "123"

                uniqueName = appName[0]
                #print uniqueName
                Count += 1
    #print Count

    findDebugLog = "Logs/Keys_2.txt"
    #uniqueName = None
    #Count = 0
    with open(findDebugLog) as file:
        for line in file:
            appName = line.split(':')

            if uniqueName != appName[0]:
                # print "123"

                uniqueName = appName[0]
                #print uniqueName
                Count += 1
    #print Count

    if Count == 0:
        Status = "PASSED "
        Comments = "No Hardcoded keys found in APKs"

    else:
        Status = "FAILED "
        Comments = str(Count) + " occurences of hardcoded keys found. Refer (Logs/Keys_*.log) for info.."
        #print Comments

    return ID, Desc, Status, Comments

#run()