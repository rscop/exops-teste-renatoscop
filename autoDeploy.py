#!/usr/bin/python
import os

# Validate Push Hook
def validatePush(commit):

	pos = commit.index('-')

	validations = checkVariables(commit[pos:])

	return validations

# Checking the Vars on Commit Message
def checkVariables(vars):

	response = {

		"ignoreLocalChanges": True,
		"autoDeploy": True,
		"changeBranche": False
	}

	# Stash local changes for -iL Tag
	if vars.count('-iL')>0:

		response["ignoreLocalChanges"] = False
	
	else:

		stashChanges()

	# No AutoDeploy changes for -nD Tag
	if vars.count('-nD')>0:

		response["autoDeploy"] = False

	else:

		deployCode()

	# Change branche for -cB Tag
	if vars.count('-cB')>0:

		response["changeBranche"] = True

		changeBranche(vars[vars.index('-cB')+4:].split()[0])

	return response

def stashChanges():
	
	os.system("sudo git stash")

	return

def deployCode():

	os.system("sudo git pull")

	return

def changeBranche(newBranche):

	os.system('sudo git checkout %s'%newBranche)

	return