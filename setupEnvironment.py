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

if platform.system() == 'Windows':
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

  ##Start the Twisted web server and configure it to control the api
  print("About to get powershell location.")
  powershellLocation = getSingleLineShellOutput("where powershell")
  print("powershellLocation is: ", powershellLocation)
  startTwistdCommand = powershellLocation + " $a = start-process -NoNewWindow powershell { "+twistdLocation+" web --wsgi customControllerAPI.app"+" } -PassThru"

  print("startTwistdCommand is: ", startTwistdCommand)
  subprocess.call(startTwistdCommand, shell=True)
  print("startTwistdCommand should be running in the background now.")

if platform.system() == 'Linux':
  #Put all commands in single shell command to avoid switching contexts with too many subshells.
  runShellCommand(
  """
  set -e
  echo About to create venv.
  python3 -m venv venv

  echo About to activate venv.
  . venv/bin/activate

  echo About to install flask.
  pip install Flask

  echo About to install requests.
  pip install requests

  echo About to install twisted.
  pip install Twisted

  export PYTHONPATH='.'
  echo Done updating PYTHONPATH: $PYTHONPATH.  About to start server.

  twistdLocation=$(which twistd)

  echo "Running ${twistdLocation} web --wsgi customControllerAPI.app  &>/dev/null &"

  ($twistdLocation web --wsgi customControllerAPI.py >/dev/null 2>&1)&

  echo startTwistdCommand should be running in the background now.
  """)
