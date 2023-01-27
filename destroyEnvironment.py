import os
import shutil
import subprocess
import re

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def getSingleLineShellOutput(commandToRun):
  proc = subprocess.Popen( commandToRun,cwd=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
  while True:
    line = proc.stdout.readline()
    if line:
      thetext=line.decode('utf-8').rstrip('\r|\n')
      decodedline=ansi_escape.sub('', thetext)
      return decodedline
    else:
      break

root_dir = r'venv'

print("About to destroy virtual environment.")
#Destroy the virtual environment by destroying the venv directory recursively
for root, dirs, files in os.walk(root_dir):

    for name in files:
            print(os.path.join(root, name)) 
            os.remove(os.path.join(root, name))
    for name in dirs:
            print(os.path.join(root, name))
            shutil.rmtree(os.path.join(root, name))
    os.rmdir(root_dir)
print("Finished destroying virtual environment.  Next, we will destroy the twistd process that runs the custom controller API.")
powershellLocation = getSingleLineShellOutput("where powershell")
#powershellLocation = subprocess.call("where powershell", shell=True)
print("powershellLocation is: ", powershellLocation)
stopTwistdCommand = str(powershellLocation) + str(' Stop-Process -Name "twistd"')
print("stopTwistdCommand is: ", stopTwistdCommand)
subprocess.call(stopTwistdCommand, shell=True)
print("The twistd process should be stopped now, which means that the custom controller should also be stopped.")


