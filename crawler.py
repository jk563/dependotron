#!/usr/bin/env python

import urllib2, re, pageOpener, MySQLdb

opener = None

def setUpOpener(key, cert):
	global opener
	opener = pageOpener.getOpener(key, cert)

def crawl(uri):
	print uri
	folder = opener.open(uri)
	if pomExists(folder):
		pom = getPom(uri)
		processPom(pom)
	try:
		subFolders = getSubFolders(uri)
		for subFolder in subFolders:
			crawl(subFolder)
	except:
		pass

def pomExists(folder):
        for line in folder:
                if "pom.xml" in line:
                        return "true"

def getPom(uri):
	pomUri = uri + "pom.xml"
	return opener.open(pomUri)

# Places known to not have POMs. branches and tags should be removed from this list. Configurable?
blacklist = ["../", "./", "LiveStats/", "src/", "branches/", "tags/" ]

def getSubFolders(uri):
	try:
		folder = opener.open(uri)
	except urllib2.URLError, e:
		sys.stderr.write('URLError occured using uri ' + uri)
		sys.stderr.write(error.strerror)
		print 'URLError occured when retrieving ' + uri + ' , see stderr for details.'
		raise
	subDirectories = []
        for line in folder:
                foundSubdirectories = re.search("href=\".+/\">", line)
		if foundSubdirectories:
				subdir = foundSubdirectories.group(0)[6:-2]
				canAdd = 1
                        	for blacklisted in blacklist:
                                	if subdir in blacklisted:
                                        	canAdd = 0
                        	if canAdd == 1:
					subDirectories.append(uri + subdir)
        return subDirectories

# VERSIONING
def processPom(pom):
	# Ordering matters! Partial parse restarts from the same point?
	thisGroup = getValue("groupId", pom)
	thisArtifact = getValue("artifactId",pom)
	thisDependent = thisGroup + "." + thisArtifact
        dependencyNodes = pullDependencies(pom)
        # Need to grab parent POM too!
	for dependency in dependencyNodes:
                dependencyArtifact = getValue("artifactId", dependency)
                dependencyGroup = getValue("groupId", dependency)
                thisDependency = dependencyGroup + "." + dependencyArtifact
                outputDependency(thisDependent,thisDependency)

# Should check if matching entry already exists.
def outputDependency(dependent, dependency):
	db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dependotron")
	cursor = db.cursor()
	cursor.execute("INSERT INTO dependencies ( dependent , dependency ) VALUES (%s, %s)", (dependent, dependency))
	db.commit()
	db.close()

def pullDependencies(pom):
        dependencies = []
        inDep = 0
        for line in pom:
                if inDep == 1:
                        if "</dependency>" in line:
                                inDep = 0
                                dependencies.append(dependency)
                        else:
                                dependency.append(line)
                if "<dependency>" in line:
                        inDep = 1
                        dependency =[]
        return dependencies

# Need to work with variables
def getValue(property, node):
        for line in node:
                if property in line:
			# Need to stop being greedy
                        foundValues = re.search(">.+<", line)
                        if foundValues:
                                return foundValues.group(0)[1:-1]
