import json
from flask import Flask, request, jsonify, make_response, abort
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
import platform
import os
import pathlib

app = Flask(__name__)

@app.route('/controller/custom/', methods=['GET'])
def get_outputs():
  #Write whatever log entries you want to be ingested into Agile Cloud Manager's logs.
  logEntries = [
    {'controllerName':'customCtlr', 'message':'First write this to log from GET.'},
    {'controllerName':'customCtlr', 'message':'Second write this to log from GET.'},
    {'controllerName':'customCtlr', 'message':'Third write this to log from GET.'}
  ]
  apiString = 'None'
  if platform.system() == 'Windows':
    apiStringLocation = os.path.expanduser("~")+'\\acm\\keys\\custom.txt'
  elif platform.system() == 'Linux':
    apiStringLocation = '/usr/acm/keys/custom.txt'
  with open(apiStringLocation) as f:
    apiString = f.readline().strip('\n')
  ##FOR TESTING ONLY: hard-coding output variables so you can see working example of 
  ## format for output.  Your actual custom controller would need code to interpolate 
  ## the values of output variables from whatever source system you are controlling.
  ## You must include at least one output variable to signal that the controller POST 
  # command has completed its run, even if the one output variable in that case is an
  # arbitrary, predefined message.
  outputVars = [
    {'varName':'firstOutputVar', 'varValue':'value-for-first-output-variable'},
    {'varName':'secondOutputVar', 'varValue':'value-for-second-output-variable'}
  ]
  #Uncomment this next line to test failing to receive output variables, 
  # which means that the POST command has not yet completed.
  #outputVars = []
  responseJson = { 
    'outputVars': outputVars,
    'logEntries': logEntries
  }
  resp = make_response(jsonify(responseJson))
  resp.headers['api-string'] = apiString
  resp.headers['content-type'] = 'application/json'  
  with open("getHeadersInit.txt", mode='w') as out:
     out.write("Inside get endpoint!\n")
     line2 = "resp.headers is: "+str(resp.headers)+"\n"
     line3 = "request.headers is: "+str(request.headers)+"\n"
     out.write(line2)
     out.write(line3)
  if (request.headers.get('Api-String') == None) and (request.headers.get('api-string') == None):
    resp.headers['api-string'] = 'None'
    abort(401, description="You failed to supply a correct api-string header value.")
  if (request.headers.get('Api-String') != None) or (request.headers.get('api-string') != None):
    if (request.headers.get('Api-String') != None):
      if str(resp.headers['api-string']) != str(request.headers['Api-String']):
        resp.headers['api-string'] = 'None'
        abort(401, description="You failed to supply the correct Api-String header value.")
    if (request.headers.get('api-string') != None):
      if str(resp.headers['api-string']) != str(request.headers['api-string']):
        resp.headers['api-string'] = 'None'
        abort(401, description="You failed to supply the correct api-string header value.")
  return resp

@app.route('/controller/custom/', methods=['POST'])
def invoke_controller():
  #Write whatever log entries you want to be ingested into Agile Cloud Manager's logs.
  logEntries = [
    {'controllerName':'customCtlr', 'message':'First write this to log from POST.'},
    {'controllerName':'customCtlr', 'message':'Second write this to log from POST.'},
    {'controllerName':'customCtlr', 'message':'Third write this to log from POST.'}
  ]
  apiString = 'None'
  if platform.system() == 'Windows':
    apiStringLocation = os.path.expanduser("~")+'\\acm\\keys\\custom.txt'
  elif platform.system() == 'Linux':
    apiStringLocation = '/usr/acm/keys/custom.txt'
  with open(apiStringLocation) as f:
    apiString = f.readline().strip('\n')
  #FOR TESTING ONLY.  Printing response to a file so you can read the results to 
  # ensure that the POST to this endpoint is working correctly.  Your actual POST 
  # handling code will instead use the contents of the payload or orchestrate whatever 
  # system your custom controller is intended to orchestrate.
  with open("postPayloadInit.txt", mode='w') as out:
     out.write("Inside post endpoint!\n")
  record = json.loads(request.data)
  responsePayload = [ 
        {"this": "block"}, 
        {"must": "be"}, 
        {"a": "list"}, 
        {"of": "valid"}, 
        {"json": "objects"}, 
        {"and": "the"},
        {"entire": "response"},
        {"must": "also be"},
        {"valid": "json."}
  ]
  responseJson = { 
    'payload': responsePayload,
    'logEntries': logEntries
  }
  resp = make_response(jsonify(responseJson))
  resp.headers['api-string'] = apiString
  resp.headers['content-type'] = 'application/json'  
  with open("postPayloadInit.txt", mode='w') as out:
     out.write(str(resp.json)+"\n")
     out.write(str(resp.headers)+"\n")
     out.write("-------------------------------------------\n")
     out.write(str(request.headers)+"\n")
     out.write("-------------------------------------------\n")
     out.write(str(record)+"\n")
  if (request.headers.get('Api-String') == None) and (request.headers.get('api-string') == None):
    resp.headers['api-string'] = 'None'
    abort(401, description="You failed to supply a correct api-string header value.")
  if (request.headers.get('Api-String') != None) or (request.headers.get('api-string') != None):
    if (request.headers.get('Api-String') != None):
      if str(resp.headers['api-string']) != str(request.headers['Api-String']):
        resp.headers['api-string'] = 'None'
        abort(401, description="You failed to supply the correct Api-String header value.")
    if (request.headers.get('api-string') != None):
      if str(resp.headers['api-string']) != str(request.headers['api-string']):
        resp.headers['api-string'] = 'None'
        abort(401, description="You failed to supply the correct api-string header value.")
  return resp

flask_site = WSGIResource(reactor, reactor.getThreadPool(), app)

root = Resource()
root.putChild(b'acm', flask_site)

reactor.listenTCP(8675, Site(root))
reactor.run()
