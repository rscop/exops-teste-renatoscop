#!flask/bin/python
from flask import Flask, abort, request, jsonify, g, url_for
import sys
import configparser
import logging
import logging.handlers
import os
from autoDeploy import validatePush, rebaseBranchs

app = Flask(__name__)


def logStart():
	logit(' __________________________________________________')
	logit('[         INICIANDO SERVICO DE AUTO DEPLOY         ]')
	logit(' --------------------------------------------------')

# SetupLOG Funnction
def setuplog(lf,lfBkpCnt,logLevel):

	global gtwlogger

	gtwlogger = logging.getLogger('GTW_LOG')

	gtwlogger.setLevel(logging.DEBUG)

	formatter = logging.Formatter('%(asctime)s-%(message)s')

	# Add the log message handler to the logger
	handler = logging.handlers.TimedRotatingFileHandler(lf, when='midnight', interval=1, backupCount=lfBkpCnt)

	handler.setFormatter(formatter)

	gtwlogger.addHandler(handler)
	
	logStart()

def logit(m):
	if config['log_mode']=='2':
		print(m)
	gtwlogger.debug(m)

# Read configurationFile
def get_ConfigFile(inifile, section):

	c = configparser.ConfigParser()

	dataset = c.read(inifile)

	if len(dataset) != 1:

		raise ValueError

	try:

		c.read(inifile)

	except Exception as e:

		raise e

	# Verify keys in configuration file
	for key in c[section]:

		if len(c[section][key]) == 0:

			fatal("fatal: %s: could not find %s string" % (inifile, key), 1)

	return c[section]

# Method for data query (Verify API Integrity)
@app.route('/gitHub', methods=['GET'])
def get():
	
	logit('Receiving GET on /gitHub')

	# Response if OK
	response = '{"status": "Consultado"}'

	logit('GET OK')
	return(response)

# GH Hook configured for acess this method
@app.route('/gitHub', methods=['POST'])
def post():

	logit('Receiving POST on /gitHub')
	content = request.get_json()
	logit('Hook from HitHub')

	try:
		branch = content["ref"].split('/')[2]
		eventType = "push"
		logit('Event Push')

	except:
		branch = content["ref"]
		eventType = content["ref_type"]

		if eventType == "branch":
			logit('Event New Branch')
			rebaseBranchs()


	if eventType == "push":
		logit('Going to Push')

		commit = content["head_commit"]["message"]

		# Validate received commit/push
		status = validatePush(commit)

		# Response for GH Console
		response = {
			"branch": branch,
			"commit_message": commit,
			"status": status
		}
		
	elif eventType == "branch":
		logit('Going to Branch')

		response = {
			"branch": branch,
			"status": "Rebased branchs"
		}
	
	logit('Event OK, sending response to GH')
	logit(response)

	return(response) 

if __name__ == '__main__':

	config = get_ConfigFile(sys.argv[0]+'.cfg', 'production')

	setuplog(config['logfile'],config['logfile_backup_count'],config['log_level'])

	logit('Log OK')
	logit('Config File OK')
	
	ip = config['listen_ip']

	port = config['listen_port']

	logit('Starting WS')
	app.run(host=ip, port=port, debug=False)
	logit('WS finished')
	