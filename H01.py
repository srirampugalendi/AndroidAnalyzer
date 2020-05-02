import subprocess
import time

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    status = p.wait()
    output, error = p.communicate()
    return output


def run():                                                      # Credentials Storage type - Hardware backed or Software only
    ID = "H01"                                                       # ID should be always 3 chars to maintain table structure in console output
    Desc = "Hardware backed storage type            "                # Desc should be less that 40 chars
    Status = "       "                                               # Status should be less than 7 Chars
    Comments = ""


    androidVersion = systemCmd('adb shell getprop ro.build.version.release')

    majorVersion = androidVersion.split('.')
    majorVersion=  majorVersion[0]
    systemCmd('adb shell input keyevent 3')  # Home button
    #print majorVersion

    '''
       Code to check test case for android 8 - Only Vanilla android 
    '''

    if majorVersion > 7:
        systemCmd('adb shell input keyevent 3')  # Home button
        time.sleep(1.2)
        systemCmd('adb shell am start -a android.settings.SETTINGS')
        time.sleep(1.2)
        systemCmd('adb shell input tap  665 115')
        time.sleep(1.2)
        systemCmd("adb shell input text 'Device Security'")
        time.sleep(1.2)
        systemCmd('adb shell input tap  350 250')
        time.sleep(1.2)
        systemCmd('adb shell input tap  350 1050')
        time.sleep(1.2)
        systemCmd('adb shell screencap -p /sdcard/screen.png')
        time.sleep(1.2)
        systemCmd('adb pull /sdcard/screen.png')
        time.sleep(1.2)
        systemCmd('adb shell rm /sdcard/screen.png')
        time.sleep(1.5)
        systemCmd('adb shell input keyevent 3')  # Home button
        time.sleep(1.2)

    '''
    Code to check test case for android 7
    '''



    ocrResult = systemCmd('curl -H "apikey:c6e8dcbc9688957" --form "file=@screen.png" https://api.ocr.space/Parse/Image')
    if "Hardware-backed" in ocrResult:
        Comments = "Device supports 'Hardware-backed' creds storage"
        Status = "PASSED "
    elif "Software Only" in ocrResult:
        Comments = "Device supports 'Software only' creds storage"
        Status = "FAILED "
    else:
        Comments = "Unable to verify. Pls check manually."
        Status = "  NR   "



    return ID, Desc, Status, Comments

#run()