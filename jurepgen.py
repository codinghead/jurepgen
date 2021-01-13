#!/usr/bin/python

from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from xml.dom import minidom
from datetime import datetime
import argparse, sys, encodings, os
import xml.etree.ElementTree as ET

def prettify(elem):
	"""Return a pretty-printed XML strong for the Element.
	"""
	rough_string = ElementTree.tostring(elem, "utf-8")
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")

def createJunitReport(filename, testsuitesname, verbose):
	"""Create a basic JUnit file with testsuites element
	"""
	if verbose:
		print("-o option: Attempting to create JUnit file")
	try:
		xmlRoot = Element("testsuites")
		xmlRoot.set("disabled", "0")
		xmlRoot.set("errors", "0")
		xmlRoot.set("failures", "0")
		xmlRoot.set("name", testsuitesname)
		xmlRoot.set("tests", "0")
		xmlRoot.set("time", "0")
		xmlRootComment = "Generated using " + __file__ + " on " + str(datetime.now().replace(microsecond=0).isoformat())
		xmlRootComment = Comment(xmlRootComment)
		xmlRoot.append(xmlRootComment)
		ElementTree(xmlRoot).write(filename, xml_declaration=True, encoding='utf-8')
	except:
		print("File error occured during -o option creating XML")
		sys.exit(2)
	return	

def createJunitTestsuite(filename, testsuitename, hostname, verbose):
	"""Add a JUnit testsuite element to existing file
	"""
	# create testsuite ID counter
	tsid = 0
	if verbose:
		print("-t option: Adding testsuite")

	try:
		tree = ET.parse(filename)
		#print(tree)
		xmlRoot = tree.getroot()
		#print(xmlRoot)

		# count number of existing testsuite elements to determine ID
		for existingts in xmlRoot.iter("testsuite"):
			tsid +=1

		if verbose:
			print("ID is: {}".format(str(tsid)))

		child = ET.Element("testsuite")
		child.set("name", testsuitename)
		child.set("tests", "0")
		child.set("disabled", "0")
		child.set("errors", "0")
		child.set("failures", "0")
		child.set("hostname", hostname)
		child.set("id", str(tsid))
		child.set("package", "")
		child.set("skipped", "0")
		child.set("time", "0")
		timenow = datetime.now().replace(microsecond=0).isoformat()
		#print(timenow)
		child.set("timestamp", timenow)
		xmlRoot.append(child)
		tree.write(filename, xml_declaration=True, encoding='utf-8')
	except:
		print("File error occured during -t option adding testuite to XML")
		sys.exit(2)
	return

def addJunitProperties(filename, verbose):
	"""Add a JUnit properties element to existing file
	"""
	if verbose:
		print("-p option: Adding properties element")

	try:
		tree = ET.parse(filename)
		#print(tree)
		xmlRoot = tree.getroot()
		#print(xmlRoot)

		#Find last testsuite element
		#count = 0
		for testsuite in xmlRoot.iter("testsuite"):
			lastts = testsuite
			#print(testsuite.tag, count)
			#count = count+1
		#print(count)

		ET.SubElement(lastts, "properties")
		#print("Added properties")
		#xmlRoot.append(lastts)
		tree.write(filename, xml_declaration=True, encoding='utf-8')
	except:
		print("File error occured during -p option adding properties to testsuite")
		sys.exit(2)
	return

def addJunitProperty(filename, propertyname, propertyvalue, verbose):
	"""Add a JUnit property and value element to existing file
	"""
	if verbose:
		print("-q option: Adding property element with name and value")

	try:
		tree = ET.parse(filename)
		#print(tree)
		xmlRoot = tree.getroot()
		#print(xmlRoot)
		#Find last properties element
		#count = 0
		for properties in xmlRoot.iter("properties"):			
			lastp = properties
			#print(properties.tag, count)
			#count = count+1
		#print(count)
		newproperty = ET.SubElement(lastp, "property")
		newproperty.attrib["name"] = propertyname
		newproperty.attrib["value"] = propertyvalue
		#print("Added property")
		#xmlRoot.append(lastts)
		tree.write(filename, xml_declaration=True, encoding='utf-8')
	except:
		print("File error occured during -q option adding property to properties")
		sys.exit(2)
	return

def addJunitTestcase(filename, name, classname, status, time, verbose):
	dummycount = 0

	if verbose:
		print("-t option: Adding testcase element")

	try:
		tree = ET.parse(filename)
		xmlRoot = tree.getroot()
		#Find last testsuite element
		for testsuite in xmlRoot.iter("testsuite"):
			dummycount += 1
		testcase = ET.SubElement(testsuite, "testcase")
		testcase.attrib["name"] = name
		# currently ignoring assertions
		testcase.attrib["assertions"] = ""
		testcase.attrib["classname"] = classname
		testcase.attrib["status"] = status
		testcase.attrib["time"] = time
		tree.write(filename, xml_declaration=True, encoding='utf-8')
	except:
		print("File error occured during -t option adding testcase")
		sys.exit(2)
	return

def main():
	verbose = False
	name = ""
	addtestsuite = False
	addtest = False
	addproperties = False
	addproperty = False
	propertyname = ""
	propertyvalue = ""
	# default hostname is localhost
	hostname = "localhost"
	message = ""
	type = ""
	status = ""
	time = ""
	description = ""
	classname = ""

	parser = argparse.ArgumentParser()
	groupone = parser.add_mutually_exclusive_group()
	groupone.add_argument("-i", "--inputfile", help="XML input file name")
	groupone.add_argument("-o", "--outputfile", help="XML output file name")

	grouptwo = parser.add_mutually_exclusive_group()
	grouptwo.add_argument("-s", "--testsuite", help="add testsuite with a -n name", action="store_true")
	grouptwo.add_argument("-p", "--properties", help="add properties to last testsuite", action="store_true")
	grouptwo.add_argument("-q", "--property", help="add named property with value to properties")
	grouptwo.add_argument("-t", "--testcase", help="add testcase with a -n name", action="store_true")

	parser.add_argument("-v", "--verbose", help="output status during operation", action="store_true")
	parser.add_argument("-n", "--name", help="name of testsuites, testsuite, or testcase")
	parser.add_argument("-w", "--propertyvalue", help="value for property option")
	parser.add_argument("-j", "--hostname", help="hostname for testsuite")
	parser.add_argument("-r", "--packagename", help="packagename for testsuite")
	parser.add_argument("-m", "--message", help="message for skipped, error or failure of testcase")
	parser.add_argument("-y", "--type", help="type for error or failure of testcase")
	parser.add_argument("-d", "--description", help="description for error or failure of testcase")

	args = parser.parse_args()

	if args.verbose:
		verbose = True
		print("Verbose Mode")

	if args.name:
		name = args.name
		if verbose:
			print("name is: {}".format(name))

	if args.hostname:
		hostname = args.hostname
		if verbose:
			print("hostame is: {}".format(hostname))

	if args.message:
		message = args.message
		if verbose:
			print("message is:{}".format(message))

	if args.propertyvalue:
		propertyvalue = args.propertyvalue
		if verbose:
			print("propertyvalue is: {}".format(propertyvalue))

	if args.testsuite:
		if verbose:
			print("Adding testsuite")
		addtestsuite = True
	elif args.properties:
		if verbose:
			print("Adding properties")
		addproperties = True
	elif args.property:
		propertyname = args.property
		if verbose:
			print("Adding property named: {}".format(propertyname))
		addproperty = True
	elif args.testcase:
		if verbose:
			print("Adding testcase")
		addtestcase = True

	if args.inputfile:
		filename = args.inputfile
		if verbose:
			print("Input file name found: {}".format(filename))

		if not os.path.exists(filename):
			print("Failure: input file does not exist {}".format(filename))
			sys.exit(2)
		if addtestsuite:
			createJunitTestsuite(filename, name, hostname, verbose)
			sys.exit()
		elif addproperties:
			addJunitProperties(filename, verbose)
			sys.exit()
		elif addproperty:
			addJunitProperty(filename, propertyname, propertyvalue, verbose)
			sys.exit()
		elif addtestcase:
			addJunitTestcase(filename, name, classname, status, time, verbose)
			sys.exit()

	elif args.outputfile:
		filename = args.outputfile
		if verbose:
			print("Output file name found: {}".format(filename))

		if os.path.exists(filename):
			print("Failure: output file exists {}".format(filename))
			sys.exit(2)

		createJunitReport(filename, name, verbose)
		sys.exit()

if __name__ == "__main__":
	main()

