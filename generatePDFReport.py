import pdfkit
import subprocess

def systemCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #status = p.wait()
    output, error = p.communicate()
    return output

def run():

    systemCmd("rmdir /S /Q Result")
    systemCmd("mkdir Result")

    options = {
        'quiet': '',
        'orientation': 'Landscape',

    }


    print "\n[+] Generating PDF report in Reports/Findings.pdf.."
    pdfkit.from_file('Logs/TestResults.txt', 'Result/Findings.pdf',options=options)
    print "\n[+] Backup Result and Logs folder for reference. It will be overwritten when the tool is run next."

#run()