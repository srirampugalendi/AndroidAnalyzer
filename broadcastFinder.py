import subprocess
from xml.dom import minidom
import time,sys

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output,error

'''
def drozerDeviceConnectivityCheck():

    while (True):
        cmd = 'adb forward tcp:31415 tcp:31415'
        op = systemCmd(cmd)
        cmd = 'drozer console connect -c "list"'
        op, err = systemCmd(cmd)
        if 'app.activity.forintent' in op:
            sys.stdout.write("\r                                                                  ")
            sys.stdout.flush()
            sys.stdout.write("\rDrozer connection established with device !")
            time.sleep(2)
            sys.stdout.flush()
            sys.stdout.write("\r                                                                  ")
            sys.stdout.flush()
            sys.stdout.write("\r Running tests..")
            sys.stdout.flush()
            return None
        else:
            sys.stdout.write("\r                                                                  ")
            sys.stdout.flush()
            sys.stdout.write("\rTurn on drozer in device.. #")
            sys.stdout.flush()
            time.sleep(0.80)
            sys.stdout.write("\r                                                                  ")
            sys.stdout.flush()
            sys.stdout.write("\rTurn on drozer in device.. ##")
            sys.stdout.flush()
            time.sleep(0.80)
            sys.stdout.write("\r                                                                  ")
            sys.stdout.flush()
            sys.stdout.write("\rTurn on drozer in device.. ###")
            sys.stdout.flush()
'''

def drozerDeviceConnectivityCheck():

    while (True):
        cmd = 'drozer console connect -c "list"'
        op, err = systemCmd(cmd)

        if 'app.activity.forintent' in op:
            sys.stdout.write("\rDrozer connection established with device !")
            time.sleep(2)
            sys.stdout.flush()
            sys.stdout.write("\r[-] Running tests..")
            sys.stdout.flush()
            return None
        else:
            sys.stdout.write("\rTurn on drozer in device.. #")
            sys.stdout.flush()
            time.sleep(0.80)
            sys.stdout.write("\rTurn on drozer in device.. ##")
            sys.stdout.flush()
            time.sleep(0.80)
            sys.stdout.write("\rTurn on drozer in device.. ###")
            sys.stdout.flush()

def run(scope):

    logfile = open("Logs/Recievers_log.txt","wb")
    withoutReciever = []
    withReciever = []
    #ApkList = "./Apks/apkList.txt"
    ApkList = scope
    count = 0

    cmd = 'adb forward tcp:31415 tcp:31415'
    op = systemCmd(cmd)

    drozerDeviceConnectivityCheck()

    logfile.write("\n\n\n##### Apps with registered broadcast receivers and their info : #####\n\n\n")
    with open(ApkList) as file:
        for line in file:
            #print line

            cmd = 'drozer console connect -c "run app.broadcast.info -a ' + line.rstrip() + '"'
            op,err = systemCmd(cmd)
            #print cmd
            #print op

            if 'No matching receivers' in op:
                #print line
                withoutReciever.append(line)

            else:
                count += 1
                withReciever.append(line)
                logfile.write(op.split("\n",2)[2])                 # op.split("\n",2)[2] split is used to remove first two lines form output as it contains junk

    #print withReciever
    #print withoutReciever

    logfile.write("\n\n\n#####Apps with registered broadcast receivers#####\n\n\n")
    for i in withReciever:
        logfile.write(i.rstrip()+"\n")

    logfile.write("\n\n\n#####Apps without any registered broadcast receivers#####\n\n\n")
    for j in withoutReciever:
        logfile.write(j.rstrip()+"\n")
        
    print("\n[!] Info : "+ str(count) + " Apks with broadcast receivers found. Verify permissions manually. Info in Logs/Recievers_log.txt")

    testResults = open("Logs/TestResults.txt", "a")
    testResults.write("\n[!] Info : "+ str(count) + " Apks with broadcast receivers found. Verify permissions manually. Info in Logs/Recievers_log.txt")
    testResults.close()

    logfile.close()

#run("./Apks/apkList.txt")

