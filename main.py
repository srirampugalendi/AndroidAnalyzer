import subprocess
import time
import os
import H01
import F01
import F02
import F03
import A01
import A07
import A09
import A11
import A15
import tqdm
import findSystemUIDapks,broadcastFinder,serviceFinder,contentFinder,generatePDFReport
import ApksExtractor,decompileApks

isIssueLabelPrinted = False
choice = 0


def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output

def enumerateDevice():

    fingerprintfile = open("Logs/TestResults.txt", "wb")
    print "[+] Enumerating device..\n"

    deviceModel = systemCmd('adb shell getprop ro.product.model')
    androidVersion = systemCmd('adb shell getprop ro.build.version.release')
    buildNumber = systemCmd('adb shell getprop ro.build.display.id')
    fingerprint = systemCmd('adb shell getprop ro.build.fingerprint')
    kernelVersion = systemCmd('adb shell uname -r')


    print 'Device Model          : ' + deviceModel.rstrip()
    print 'Android Version       : ' + androidVersion.rstrip()
    print 'Build Number          : ' + buildNumber.rstrip()
    print 'Fingerprint           : ' + fingerprint.rstrip()
    print 'Kernel Version        : ' + kernelVersion.rstrip()

    fingerprintfile.write('Device Model          : ' + deviceModel)
    fingerprintfile.write('Android Version       : ' + androidVersion)
    fingerprintfile.write('Build Number          : ' + buildNumber)
    fingerprintfile.write('Fingerprint           : ' + fingerprint)
    fingerprintfile.write('Kernel Version        : ' + kernelVersion)

    fingerprintfile.close()

def checkAdb():
    print "[+] Waiting for a device..(Connect a adb enabled android device)"
    command = "adb devices"
    output = systemCmd(command)
    while True:
        if output == "List of devices attached\r\n\r\n" or output == "List of devices attached\n\n":
            time.sleep(2)
            #print "Waiting for Device"
            output = systemCmd(command)
        elif output.count("\r\n") > 3:
            print "[+] Error! Please check adb connectivity and ensure that only one devices is connected."
            print "[+] Quitting program."
            exit()
        else:
            print "[+] Device Connected.."
            break

def getUserChoice():

    '''
    Code not implemented
    '''

    print "Select an option to continue.."
    print "1. Scan only org apks in device"
    print "2. Scan only non org apks in device"
    print "3. Scan all apks in device"
    print "4. Scan apks in ./Apks folder"
    choice = raw_input('Enter your choice: ')
    choice = str(choice)
    return choice

def printTestResults(issueId, issueDesc, testStatus, issueComments):


    global  isIssueLabelPrinted
    testResults = open("Logs/TestResults.txt", "a")

    if isIssueLabelPrinted == False:
        print ("\nID  | Description                              | Status  | Comments ")
        testResults.write("\nID  | Description                              | Status  | Comments \n")
        isIssueLabelPrinted = True

    print issueId + " | " +issueDesc +" | "+ testStatus + " | " + issueComments
    testResults.write(issueId + " | " +issueDesc +" | "+ testStatus + " | " + issueComments + "\n")
    testResults.close()

def statusDesc():
    print "\nStatus Description :"
    print "PASSED = Not vulnerable to the issue"
    print "FAILED = Vulnerable to the issue"
    print "NR     = Needs review manually"

    testResults = open("Logs/TestResults.txt", "a")
    testResults.write("\nStatus Description :\n")
    testResults.write("PASSED = Not vulnerable to the issue\n")
    testResults.write("FAILED = Vulnerable to the issue\n")
    testResults.write("NR     = Needs review manually\n")
    testResults.close()

def installApks():
    print "\n[+] Installing apks.."
    Count = 0
    systemCmd("dir .\Apks /b > ./Apks/apkList.txt");
    ApkList = "./Apks/apkList.txt"
    nonDeviceApksfd = open("nonDeviceApks.txt", "wb")
    with open(ApkList) as file:
        for line in file:
            if ".apk" in line:
                Count += 1

    if Count == 0:
        print "[!] Apks folder is empty! Quitting !"
        exit()

    with open(ApkList) as file:
        #pbar = tqdm.tqdm(total=Count)
        for line in file:
            #pbar.update(1)
            #print line
            if ".apk" in line:

                cmd = "adb install \"./Apks/" + line.rstrip() + "\""
                op = systemCmd(cmd)
                #print cmd
                #print op
                cmd = "aapt dump badging \"Apks/" + line.rstrip() + "\" | findstr \"package\""
                op = systemCmd(cmd)
                #print op
                packagename = op.split("'")
                nonDeviceApksfd.write(packagename[1] + "\n")
    nonDeviceApksfd.close()
    print "[+] Done installing.."

systemCmd("rmdir /S /Q Logs")
systemCmd("mkdir Logs")

checkAdb()
enumerateDevice()
choice = getUserChoice()

if choice == '1':
    scope = 'Org_Apks.txt'

elif choice == '2':

    scope = 'NonOrg_Apks.txt'
elif choice == '3':
    scope = 'All_Apks.txt'
elif choice == '4':
    scope = 'folder'
else:
    print "Invalid Choice"
    exit()

if scope == 'folder':
    scope = "nonDeviceApks.txt"
    installApks()
else:
    ApksExtractor.run(scope)


decompileApks.run()


''' Call Hardware testcases'''

a,b,c,d =H01.run()
printTestResults(a,b,c,d)

''' Call Firmware testcases'''

Id, Desc, Status, Comments =F01.run()
printTestResults(Id, Desc, Status, Comments)

Id, Desc, Status, Comments =F02.run()
printTestResults(Id, Desc, Status, Comments)

Id, Desc, Status, Comments =F03.run()
printTestResults(Id, Desc, Status, Comments)

''' Call Apps testcases'''

Id, Desc, Status, Comments =A01.run()
printTestResults(Id, Desc, Status, Comments)


Id, Desc, Status, Comments =A07.run(scope)
printTestResults(Id, Desc, Status, Comments)

Id, Desc, Status, Comments =A09.run()
printTestResults(Id, Desc, Status, Comments)

Id, Desc, Status, Comments =A11.run()
printTestResults(Id, Desc, Status, Comments)

Id, Desc, Status, Comments =A15.run()
printTestResults(Id, Desc, Status, Comments)

''' Call Comm Interface testcases'''

'''Call info testcases'''

statusDesc()
findSystemUIDapks.run()
broadcastFinder.run(scope)
serviceFinder.run(scope)
contentFinder.run(scope)
generatePDFReport.run()
