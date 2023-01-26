import requests
import time

timeOutMins = 5
numIntervals = timeOutMins*6

######################################################################
##### GET code will be formed from the below
######################################################################
def getOutputs(myurl, counter=0):
  headers = {'content-type': 'application/json'}
  print("About to GET")
  res = requests.get(myurl, headers=headers)
  print("GET res is: ", str(res))
  print("GET res.status_code is: ", res.status_code)
  print("GET res.headers are: ", res.headers)
  print("GET res.json is: ", str(res.json()))

  if res.status_code == 102: #This indicates the custom controller is in process and has not yet returned a response.
    #Iterate from 1 to numIntervals
    if counter < (numIntervals+1):
      print("Custom controller is still processing after ", str(counter*10), " seconds. Will continue to retry. ")
      time.sleep(10)
      counter +=1
      getOutputs(myurl, counter)
    else:
      print("ERROR: GET request to custom controller did not return a 200 response even after retrying for ", timeOutMins, " minutes. Check you cloud provider portal to make sure there are no orphaned resources.  Also, consider re-running the command again and consider posting a request on our GitHub site for the time out interval to be increased.  ")
      exit(1)

  if res.status_code == 400: #This is where the server replies that the client had an error such as a malformed request.
    print("GET 400 Error")
    print("GET res.json is: ", str(res.json()))
    print("ERROR: A 400 response was returned by the controller.  Please examine the logs to determine the root cause.  ")
    exit(1)

  if res.status_code == 200: #This indicates success.
    print("-------------------- GET res is 200 ok. ------------------------")
    print("GET res.json is: ", str(res.json()))
    for item in res.json():
      print("item is: ", item)

  if res.status_code == 500: #This indicates an error from the server.
    print("GET 500 Error")
    #Iterate from 1 to numIntervals
    if counter < (numIntervals+1):
      print("Custom controller received a 500 response from the controller after ", str(counter*10), " seconds. Continuing to retry.  ")
      time.sleep(10)
      counter +=1
      getOutputs(myurl, counter)
    else:
      print("ERROR: GET request to custom controller did not return a 200 response even after retrying for ", timeOutMins, " minutes. Check your cloud provider portal to make sure there are no orphaned resources.  Also, consider re-running the command again and consider posting a request on our GitHub site for the time out interval to be increased.  ")
      exit(1)



####################################################################
#### POST code will be formed from the below.
####################################################################
def postCommand(myurl, counter=0):
  import json
  print("About to do POST")
  postJson = { 
    'command': 'on', 
    'variables': [ 
        {"this": "file"}, 
        {"must": "be"}, 
        {"a": "list"}, 
        {"of": "valid"}, 
        {"json": "objects"}, 
        {"and": "this"},
        {"entire": "file"},
        {"must": "also be"},
        {"valid": "json."}
    ]
  }
  headers = {'content-type': 'application/json'}
  res = requests.post(myurl, json.dumps(postJson), headers=headers)
  print("POST res is: ", str(res))
  print("POST res.status_code is: ", res.status_code)
  print("POST res.headers are: ", res.headers)
  if res.status_code == 200: #This indicates success.
    print("-------------------- POST res is 200. ------------------------")
    print("POST res.json is: ", str(res.json()))

  if res.status_code == 400: #This indicates success.
    print("-------------------- POST res is 400. ------------------------")
    print("POST res.json is: ", str(res.json()))

  if res.status_code == 500: #This indicates an error from the server.
    print("-------------------- POST res is 500. ------------------------")
    print("POST res.json is: ", str(res.json()))
    #Iterate from 1 to numIntervals
    if counter < (numIntervals+1):
      print("Custom controller received a 500 response from the controller after ", str(counter*10), " seconds. Continuing to retry.  ")
      time.sleep(10)
      counter +=1
      postCommand(myurl, counter)
    else:
      print("ERROR: GET request to custom controller did not return a 200 response even after retrying for ", timeOutMins, " minutes. Check your cloud provider portal to make sure there are no orphaned resources.  Also, consider re-running the command again and consider posting a request on our GitHub site for the time out interval to be increased.  ")
      exit(1)

myurl = "http://localhost:8675/acm/controller/custom/"
postCommand(myurl)
getOutputs(myurl)

