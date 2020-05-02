import subprocess
import tqdm
import time

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output

def run(scope):
    '''
    The file with the output of 'adb shell pm list packages > Full_Package_List.txt' is prerequisite for this code
    THIS SCRIPT WORKS ONLY IN UBUNTU - AS GREP COMMAND IS USED
    '''
    # Code to take full apk list from device, separate & extract org specific APKs

    print '\n[+] Generating full packages list..'
    systemCmd('adb shell pm list packages > Full_Package_List.txt')
    #print '[+] Separating org APKs..'                                # Apps are separated based on keyword google and facebook in apk name
    fd_OrgApks = open("Org_Apks.txt", "wb")
    fd_NonOrgApks = open("NonOrg_Apks.txt", "wb")
    fd_AllApks = open("All_Apks.txt", "wb")
    fd_FullPackageList = "Full_Package_List.txt"
    totalAppCount = 0
    OrgAppCount = 0
    nonOrgAppCount = 0
    with open(fd_FullPackageList) as file:
        for line in file:
            packageName = line.split(':')
            if packageName[0] == 'package':
                totalAppCount += 1
                packageName = packageName[1]
                if "google" in packageName.lower() or "facebook" in packageName.lower():
                    fd_OrgApks.write(packageName)
                    fd_AllApks.write(packageName)
                    OrgAppCount += 1
                else:
                    fd_NonOrgApks.write(packageName)
                    fd_AllApks.write(packageName)
                    nonOrgAppCount += 1
    print '[+] Found ' + str(totalAppCount) + ' total installed apps including ' + str(OrgAppCount) + ' org apps..'
    fd_OrgApks.close()
    fd_NonOrgApks.close()

    #Code for Extracting org apks

    fd_PackageList = scope
    print '[+] Begining extraction of APKs to /sdcard/Apks..\n'
    systemCmd("adb shell rm -r /sdcard/Apks")
    systemCmd("adb shell mkdir /sdcard/Apks")
    # systemCmd("adb shell rm /sdcard/Apks/*.apk")

    totalcount = 0
    if scope == 'Org_Apks.txt':
        totalcount=OrgAppCount
    elif scope == 'NonOrg_Apks.txt':
        totalcount=nonOrgAppCount
    else:
        totalcount = OrgAppCount + nonOrgAppCount


    with open(fd_PackageList) as file:
        pbar = tqdm.tqdm(total=totalcount)
        for line in file:
            pbar.update(1)
            cmdOutput = systemCmd('adb shell pm path ' + line)
            path = cmdOutput[8:]
            # print path
            # print '    Extracting ' + line.rstrip() + ' from ' + path.rstrip()
            apkname = path.split('/')
            apkname = apkname[len(apkname)-2]
            #print apkname
            cmd = "adb shell cp " + path.rstrip() + " /sdcard/Apks/" + apkname + ".apk"
            #print cmd
            systemCmd(cmd)
            # cmd = 'adb pull ' + path.rstrip() + ' .'
            # print cmd
            # time.sleep(2)
            # systemCmd(cmd)


    systemCmd("rmdir /S /Q Apks")
    systemCmd("mkdir Apks")
    print '\n\n[+] Copying Apks to ./Apks'
    systemCmd("adb pull /sdcard/Apks/ .")
    systemCmd("adb shell rm -r /sdcard/Apks")
    print '[+] Finishing up.'
    print '[+] Completed.'

#run("Org_Apks.txt")