import subprocess
import re
import os

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

#Create a virtual environment with venv
runShellCommand("py -3 -m venv venv")

##Activate venv
runShellCommand("venv\Scripts\\activate")

##Install flask for api, requests to call api, and Twisted to host api
runShellCommand("pip install Flask")
runShellCommand("pip install requests")
runShellCommand("pip install Twisted")

##Set environment variable for the API
os.environ['PYTHONPATH'] = '.'
print("Done updating PYTHONPATH.  About to start server.")

##Start the Twisted web server and configure it to control the api
runShellCommand("twistd web --wsgi customControllerAPI.app")
runShellCommand("twistd -n web --port tcp:8080 --wsgi customControllerAPI.app")
#Note: The terminal may look in a held-up state after these commands because 
#twstd is running in the foreground without output.  To confirm the api is running, 
#you can run the makeApiCall.py program.
