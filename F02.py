import subprocess

outdatedAndroidVersions = [
    '4.0',
    '4.1',
    '4.2',
    '4.3',
    '4.4',
    '5.0',
    '5.1',
    '6.0',
    '7.0',
    '7.1',
];

latestAndroidVersion = ['8.0','8.1',];

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output

def run():
    ID = "F02"                                         # ID should be always 3 chars to maintain table structure in console output
    Desc = "Device runs outdated version of Android "  # Desc should be less that 40 chars
    Status = "       "                                 # Status should be less than 7 Chars
    Comments = ""
    command = "adb shell getprop ro.build.version.release"
    output = systemCmd(command)
    #print output
    Latest=bool
    for x in latestAndroidVersion:
        if x in output:
            Latest = True
            break
        else:
            Latest = False

    #print Latest

    if Latest == True:
        Status = "PASSED "
    else:
        Status = "FAILED "

    Comments = "Device runs Android Version " + output.rstrip()

    return ID, Desc, Status, Comments