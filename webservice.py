#!flask/bin/python
from flask import Flask, abort, request, jsonify, g, url_for
import sys
import configparser
import os
from autoDeploy import *

app = Flask(__name__)

# Funcao que le arquivo de configuracoes
def get_ConfigFile(inifile, section):
	c = configparser.ConfigParser()
	dataset = c.read(inifile)
	if len(dataset) != 1:
		raise ValueError

	try:
		c.read(inifile)
	except Exception:
		raise e

	# Verifca as keys do arquivo de configuracao
	for key in c[section]:
		if len(c[section][key]) == 0:
			fatal("fatal: %s: could not find %s string" % (inifile, key), 1)

	return c[section]

# Metodo para consulta dos dados
@app.route('/gitHub', methods=['GET'])
def get():

	# Armazeno a resposta
	response = '{"status": "Consultado"}'

	return(response)

@app.route('/gitHub', methods=['POST'])
def post():

	content = request.get_json()
	branche = content["ref"].split('/')[2]
	commit = content["head_commit"]["message"]

	status = validatePush(commit)
		
	response = {
		"branche": branche,
		"message": commit,
		"status": status
	}
	return(response) 

if __name__ == '__main__':

	config = get_ConfigFile(sys.argv[0]+'.cfg', 'production')
	ip = config['listen_ip']
	port = config['listen_port']

	app.run(host=ip, port=port, debug=False)
	