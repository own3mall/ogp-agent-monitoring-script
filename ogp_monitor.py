#!/usr/bin/env python
# By OwN-3m-All <own3mall@gmail.com>
# For use with the Open Game Panel https://opengamepanel.org
# Checks to make sure OGP agents are running properly
# Sends an email to the configured address (assuming a MTA has been installed on your server) if any of your OGP servers are down.
# Prereqs:
# sudo pip install xxtea-py
# sudo pip install cffi
import xmlrpclib
import xxtea
import base64
import socket
import subprocess
import urllib2
import time
from threading import Thread
from Queue import Queue

############################
#  Variables               #
############################
checkOGPServers='127.0.0.1,12679,1234;' ## Takes the format of OGP_AGENT_IP,OGP_AGENT_PORT,OGP_AGENT_KEY ## Multiple entries are separated by the semi-colon character ";" ## EXAMPLE:   OGP_AGENT_IP,OGP_AGENT_PORT,OGP_AGENT_KEY;OGP_AGENT_IP,OGP_AGENT_PORT,OGP_AGENT_KEY;OGP_AGENT_IP,OGP_AGENT_PORT,OGP_AGENT_KEY;OGP_AGENT_IP,OGP_AGENT_PORT,OGP_AGENT_KEY;
downOGP = list()
concurrent = 400
num_threads = 30
debug = 0
email = "youremailaddress@yourdomain.com"
socket.setdefaulttimeout(10)

############################
#  Functions               #
############################

def doWork():
	while True:
		x = q.get()
		info = x.split(",")
		if len(info) == 3:
			result = checkIfOGPAgentUP(info[0], info[1], info[2])
			if str(result) == '0':
				print "OGP is up on " + str(info[0]) + ":" + str(info[1]) + "!"
			else:
				print "OGP is down on " + str(info[0]) + ":" + str(info[1]) + "! " + "Result was " + str(result)
				downOGP.append(str(info[0]) + ":" + str(info[1]))
		q.task_done()

def checkIfOGPAgentUP(ip, port, key):
	enc = xxtea.encrypt(base64.b64encode('hello'), key)
	enc = base64.b64encode(enc)
	try:
		s = xmlrpclib.ServerProxy('http://' + ip + ':' + port)
		return s.quick_chk(enc)
	except:
		return 1

############################
#  Main APP                #
############################
if checkOGPServers:
	
	entries = checkOGPServers.split(";")
	
	# Run threads
	start = time.time()
	q = Queue(concurrent * 2)
	for i in range(concurrent):
		t = Thread(target=doWork)
		t.daemon = True
		t.start()
	try:
		for x in entries:
			q.put(x)
		q.join()
	except KeyboardInterrupt:
		sys.exit(1)
	end = time.time()	
	
	# Send email for down agents
	if len(downOGP):
		print "Sending notification email!"
		commandStr = 'mail -s "OGP Agent is Down" "' + email + '" <<< "' + "\n".join(downOGP) + '"'
		if debug == 1:
			print "Using the following mail command: " + commandStr
		subprocess.Popen(commandStr,shell=True,executable="bash")
