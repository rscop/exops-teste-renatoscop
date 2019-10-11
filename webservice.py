#!flask/bin/python
from flask import Flask, abort, request, jsonify, g, url_for
import sys
import configparser
import os
from autoDeploy import validatePush

app = Flask(__name__)

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

	# Response if OK
	response = '{"status": "Consultado"}'

	return(response)

# GH Hook configured for acess this method
@app.route('/gitHub', methods=['POST'])
def post():

	content = request.get_json()

	try:
		branche = content["ref"].split('/')[2]
	except:
		eventType = content["ref_type"]
		branche = content["ref"]

	commit = content["head_commit"]["message"]

	# Validate received commit/push
	status = validatePush(commit)

	# Response for GH Console
	response = {
		"branche": branche,
		"commit_message": commit,
		"status": status
	}
	
	return(response) 

if __name__ == '__main__':

	config = get_ConfigFile(sys.argv[0]+'.cfg', 'production')

	ip = config['listen_ip']

	port = config['listen_port']

	app.run(host=ip, port=port, debug=False)
	