import subprocess
import re
import os
import platform

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def runShellCommand(commandToRun):
  proc = subprocess.Popen( commandToRun,cwd=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
  while True:
    line = proc.stdout.readline()
    if line:
      thetext=line.decode('utf-8').rstrip('\r|\n')
      decodedline=ansi_escape.sub('', thetext)
      print(decodedline)
    else:
      break

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

#Create a virtual environment with venv
print("About to create venv.")
runShellCommand("py -3 -m venv venv")

##Activate venv
print("About to activate venv.")
runShellCommand("venv\Scripts\\activate")

##Install flask for api, requests to call api, and Twisted to host api
print("About to install flask.")
runShellCommand("pip install Flask")
print("About to install requests.")
runShellCommand("pip install requests")
print("About to install twisted.")
runShellCommand("pip install Twisted")

##Set environment variable for the API
os.environ['PYTHONPATH'] = '.'
print("Done updating PYTHONPATH.  About to start server.")

twistdLocation = getSingleLineShellOutput("where twistd")
#createServiceCommand = 'sc create TwistedFlaskApp binPath= "C:\\Users\\user8\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\twistd.exe web --wsgi --customControllerAPI.app"'
#createServiceCommand = 'sc create TwistedFlaskApp binPath= "'+twistdLocation.replace("\\","\\\\")+' web --wsgi customControllerAPI.app"'
#runShellCommand(createServiceCommand)
#runShellCommand("sc start TwistedFlaskApp")
#print("twistdLocation is: ", twistdLocation.replace("\\","\\\\"))

print("platform.system() is: ", str(platform.system()))
##Start the Twisted web server and configure it to control the api
if platform.system() == 'Windows':
  #runShellCommand("twistd web --wsgi customControllerAPI.app")
  print("About to get powershell location.")
  powershellLocation = getSingleLineShellOutput("where powershell")
  print("powershellLocation is: ", powershellLocation)
  #startTwistdCommand = powershellLocation + " twistd web --wsgi customControllerAPI.app &"
  #Next line says it started job but the api cannot be accessed.
  #startTwistdCommand = powershellLocation + " Start-Job { "+twistdLocation+" web --wsgi customControllerAPI.app }"
  #"$a = start-process -NoNewWindow powershell {timeout 10; 'done'} -PassThru"
  #Next line works, but the problem is the process persists after the venv is destroyed.
  startTwistdCommand = powershellLocation + " $a = start-process -NoNewWindow powershell { "+twistdLocation+" web --wsgi customControllerAPI.app"+" } -PassThru"
if platform.system() == 'Linux':
  startTwistdCommand = twistdLocation+" web --wsgi customControllerAPI.app  &>/dev/null & "
  #command &>/dev/null &

print("startTwistdCommand is: ", startTwistdCommand)
#subprocess.call('C:\Windows\System32\powershell.exe Get-Process', shell=True)
subprocess.call(startTwistdCommand, shell=True)
print("startTwistdCommand should be running in the background now.")
# You can list all running processes with Get-Process
#Get-Process twistd
#Stop-Process -Name "twistd"
#Note: The terminal may look in a held-up state after these commands because 
#twstd is running in the foreground without output.  To confirm the api is running, 
#you can run the makeApiCall.py program.

#sc.exe [<servername>] create [<servicename>] [type= {own | share | kernel | filesys | rec | interact type= {own | share}}] [start= {boot | system | auto | demand | disabled | delayed-auto}] [error= {normal | severe | critical | ignore}] [binpath= <binarypathname>] [group= <loadordergroup>] [tag= {yes | no}] [depend= <dependencies>] [obj= {<accountname> | <objectname>}] [displayname= <displayname>] [password= <password>]

#sc.exe create customControllerAPI start= demand [binpath= <binarypathname>] [group= <loadordergroup>] [tag= {yes | no}] [depend= <dependencies>] [obj= {<accountname> | <objectname>}] [displayname= <displayname>] [password= <password>]

#sc create PythonApp binPath= "C:\Python34\Python.exe --C:\tmp\pythonscript.py"


#C:\Users\user8\AppData\Local\Programs\Python\Python310\Scripts\twistd.exe
