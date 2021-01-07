#!/usr/bin/python

from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
#from xml.etree import ElementTree
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

def createJunitTestsuite(filename, testsuitename, verbose):
	"""Add a JUnit testsuite element to existing file
	"""
	if verbose:
		print("-t option: Adding testsuite")

	try:
		tree = ET.parse(filename)
		xmlRoot = tree.getroot()
		child = ET.Element("testsuite")
		child.set("name", testsuitename)
		child.set("tests", "0")
		child.set("disabled", "0")
		child.set("errors", "0")
		child.set("failures", "0")
		child.set("hostname", "")
		child.set("id", "")
		child.set("package", "")
		child.set("skipped", "0")
		child.set("time", "0")
		timenow = datetime.now().replace(microsecond=0).isoformat()
		print(timenow)
		child.set("timestamp", timenow)
		xmlRoot.append(child)
		tree.write(filename, xml_declaration=True, encoding='utf-8')
	except:
		print("File error occured during -t option adding testuite to XML")
		sys.exit(2)
	return

def main():
	verbose = False
	name = ""
	addtestsuite = False
	addtest = False

	parser = argparse.ArgumentParser()
	groupone = parser.add_mutually_exclusive_group()
	groupone.add_argument("-i", "--inputfile", help="XML input file name")
	groupone.add_argument("-o", "--outputfile", help="XML output file name")
	parser.add_argument("-v", "--verbose", help="output status during operation", action="store_true")
	parser.add_argument("-n", "--name", help="name of testsuites, testsuite or test")
	grouptwo = parser.add_mutually_exclusive_group()
	grouptwo.add_argument("-s", "--testsuite", help="add testsuite", action="store_true")
	grouptwo.add_argument("-t", "--test", help="add test", action="store_true")
	args = parser.parse_args()

	if args.verbose:
		verbose = True
		print("Verbose Mode")

	if args.name:
		name = args.name
		if verbose:
			print("name is: {}".format(name))

	if args.testsuite:
		if verbose:
			print("Adding testsuite")
		addtestsuite = True
	elif args.test:
		if verbose:
			print("Adding test")
		addtest = True

	if args.inputfile:
		filename = args.inputfile
		if verbose:
			print("Input file name found: {}".format(filename))

		if not os.path.exists(filename):
			print("Failure: input file does not exist {}".format(filename))
			sys.exit(2)
		if addtestsuite:
			createJunitTestsuite(filename, name, verbose)
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

