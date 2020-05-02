import subprocess



def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output





def run():

    ID = "A15"                                         # ID should be always 3 chars to maintain table structure in console output
    Desc = "Older SDK version supported             "  # Desc should be less that 40 chars
    Status = "       "                                 # Status should be less than 7 Chars
    Comments = ""

    minSDKVersion = 24 # define the minimum SDK version to check for


    ApkList = "./Apks/apkList.txt"
    count = 0
    fd_minSDKApks = open("Logs/MinSDK_List.txt", "wb")
    fd_minSDKApks.write("**** Apks with minSDK less than 24 ****\n\n")
    with open(ApkList) as file:
        for line in file:
            # print line
            if ".apk" in line:
                # cmd = r"jadx\bin\jadx.bat Apks/"+line
                apkname =  line.rstrip()
                #op = "keytool -printcert -jarfile Apks/" + apkname + " | findstr /s SHA1"
                op = "aapt l -a \"Apks/" + apkname + "\" | findstr /s android:minSdkVersion"
                #print op

                #ver3 = int(ver2, 16)
                fp = systemCmd(op)
                #print fp
                ver1 = fp.split('0x')                           #op retured has min sdk version in hex as the last value in the string
                ver2 = ver1[-1]                                 #taking the last value in the list which is the hex value of minsdkversion
                version = ver2.rstrip()                         #stripping /r/n
                #print apkname
                #print fp
                #print version
                if  len(version) == 0 or len(version) == 1:
                    version = '0' + version

                version =  int("0x"+version, 16)                #converting hex to int
                #print version
                if version < minSDKVersion:
                    #print "Older SDK version supported"
                    count += 1
                    fd_minSDKApks.write(apkname+"\n")

    if count > 0:
        Status = "FAILED "  # Status should be less than 7 Chars
        Comments = str(count) + " Apks support SDK versions less than " + str(minSDKVersion)
    else:
        Status = "PASSED "  # Status should be less than 7 Chars
        Comments = "All Apks support SDK versions greater than " + str(minSDKVersion)

    return ID, Desc, Status, Comments

#run()