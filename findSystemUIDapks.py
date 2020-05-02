import subprocess

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output





def run():


    ''' Code to check Org Apks'''

    ApkList = "./Apks/apkList.txt"
    count = 0
    systemUIDApps = open("Logs/SystemUIDApks_list.txt","wb")
    systemUIDApps.write("Apps that run with privileged 'SYSTEM' permissions:" + "\n")
    with open(ApkList) as file:
        for line in file:
            # print line
            if ".apk" in line:
                # cmd = r"jadx\bin\jadx.bat Apks/"+line
                apkname = line.rstrip()
                # op = "keytool -printcert -jarfile Apks/" + apkname + " | findstr /s SHA1"
                op = "aapt l -a Apks/" + apkname + " | findstr /s android.uid.system"
                # print op
                fp = systemCmd(op)
                #print apkname
                #print fp
                if 'android.uid.system' in fp:
                    count += 1
                    systemUIDApps.write(apkname+"\n")

    systemUIDApps.close()

    print "\n\n[!] Info : " + str(count) + " APKs are installed which run with system permissions. More info in 'Logs/SystemUIDApks_list.txt'"

    testResults = open("Logs/TestResults.txt", "a")
    testResults.write("\n\n[!] Info : " + str(count) + " APKs are installed which run with system permissions. More info in 'Logs/SystemUIDApks_list.txt'")
    testResults.close()

    #

#run()