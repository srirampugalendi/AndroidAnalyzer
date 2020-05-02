import subprocess
import datetime
from datetime import date

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output

def run():

    ID = "F03"                                         # ID should be always 3 chars to maintain table structure in console output
    Desc = "Latest Security Patch                   "  # Desc should be less that 40 chars
    Status = "       "                                 # Status should be less than 7 Chars
    Comments = ""

    command="adb shell getprop ro.build.version.security_patch"
    patchDate=systemCmd(command)
    patchDateCopy=patchDate


    patchDate=patchDate.rstrip()
    patchDate = patchDate.split('-')
    #print patchDate
    patchYear = patchDate[0]
    patchMonth = patchDate[1]
    patchDay = patchDate[2]
    #print patchDay, patchMonth, patchYear

    currentDate = datetime.datetime.now()
    currentYear = currentDate.year
    currentMonth = currentDate.month
    currentDay = currentDate.day
    #print currentDay, currentMonth, currentYear

    patch = date(int(patchYear), int(patchMonth), int(patchDay))
    current = date(int(currentYear),int(currentMonth), int(currentDay))
    delta = current - patch
    #print delta.days

    if delta.days > 60:
        Status = "FAILED "
    else:
        Status = "PASSED "

    Comments = "Security Patch Level " + patchDateCopy.rstrip()
    return  ID, Desc, Status, Comments

