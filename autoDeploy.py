#!/usr/bin/python
import os

# Validate Push Hook
def validatePush(commit):

	try:

		pos = commit.index('-')

	except:
		
		pos = 0

	validations = checkVariables(commit[pos:])

	return validations

# Checking the Vars on Commit Message
def checkVariables(vars):

	response = {
		# Default values for validations
		"ignoreLocalChanges": True,
		"autoDeploy": True,
		"changeBranch": False
	}

	# Change branch for -cB Tag
	if vars.count('-cB')>0:

		response["changeBranch"] = True

		changeBranch(vars[vars.index('-cB')+4:].split()[0])

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

	return response

def stashChanges():
	
	os.system("sudo git stash")

	return

def deployCode():

	os.system("sudo git pull")

	return

def changeBranch(newBranch):

	os.system('sudo git checkout %s'%newBranch)

	return

def rebaseBranchs():

	os.system('sudo git rebase')

	return