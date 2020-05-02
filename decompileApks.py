import subprocess
import tqdm
import time

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output

def run():
    systemCmd("dir .\Apks /b > ./Apks/apkList.txt");
    systemCmd("dir .\NonOrgApks /b > ./NonOrgApks/apkList.txt");
    #print '[+] Preparing decompilation.'
    print '[+] Starting Decompilation..\n'

    Count = 0
    ApkList = "./Apks/apkList.txt"

    with open(ApkList) as file:
        for line in file:
            if ".apk" in line:
                Count += 1



    systemCmd("rmdir /S /Q decompiledApks")
    systemCmd("mkdir decompiledApks")
    systemCmd("rmdir /S /Q decompiledSource")
    systemCmd("mkdir decompiledSource")
    systemCmd("rmdir /S /Q disassembledSource")
    systemCmd("mkdir disassembledSource")

    with open(ApkList) as file:
        pbar = tqdm.tqdm(total=Count)
        for line in file:
            pbar.update(1)
            #print line
            if ".apk" in line:

                # cmd = r"jadx\bin\jadx.bat Apks/"+line
                opname = line.split('.apk')
                opFolderName = opname[0]
                opFolderNameFull = "\"decompiledApks/" + opFolderName + ".jar\""

                #'''dex to jar conversion'''

                cmd = "dex2jar\d2j-dex2jar.bat -f -o " + opFolderNameFull +  " \"Apks/" + line.rstrip() + "\""
                #print cmd
                op = systemCmd(cmd)
                #print op

                #''' jar to class files - decompiling jar'''

                cmd = "jd-cli\jd-cli.bat -od \"decompiledSource/" + opFolderName + "\" " + opFolderNameFull
                op = systemCmd(cmd)
                #print cmd

                # ''' running apktook for disassembling and getting manifest file

                cmd = "java -jar apktool.jar d \"Apks/" + line.rstrip() + "\" -o \"disassembledSource/" + opFolderName + "\""
                op = systemCmd(cmd)
                #print cmd

    print '\n\n[+] Done.' #'Info: Few Android 8.0 apps may not decompile as dex2jar does not support it'

#run()