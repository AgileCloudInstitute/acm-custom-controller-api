import json
from flask import Flask, request, jsonify
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

app = Flask(__name__)

@app.route('/controller/custom/', methods=['GET'])
def get_outputs():
  #FOR TESTING ONLY: hard-coding output variables so you can see working example of 
  # format for output.  Your actual custom controller would need code to interpolate 
  # the values of output variables from whatever source system you are controlling.
  outputVars = [
    {'varName':'firstOutputVar', 'varValue':'value-for-first-output-variable'},
    {'varName':'secondOutputVar', 'varValue':'value-for-second-output-variable'}
  ]
  return jsonify(outputVars)

@app.route('/controller/custom/', methods=['POST'])
def invoke_controller():
  #FOR TESTING ONLY.  Printing payload to a file so you can read the results to 
  # ensure that the POST to this endpoint is working correctly.  Your actual POST 
  # handling code will instead use the contents of the payload or orchestrate whatever 
  # system your custom controller is intended to orchestrate.
  with open("postPayloadInit.txt", mode='w') as out:
     out.write("Inside post endpoint!\n")
  record = json.loads(request.data)
  print("record is: ", str(record))
  with open("postPayloadInit.txt", mode='w') as out:
     out.write(str(record)+"\n")
  return jsonify(record)

flask_site = WSGIResource(reactor, reactor.getThreadPool(), app)

root = Resource()
root.putChild(b'acm', flask_site)

reactor.listenTCP(8675, Site(root))
reactor.run()
