#!/usr/bin/python

from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
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
	"""Create a JUnit testsuites element
	"""
	testsuites = Element("testsuites")
	testsuites.set("disabled", "0")
	testsuites.set("errors", "0")
	testsuites.set("failures", "0")
	testsuites.set("name", testsuitesname)
	testsuites.set("tests", "0")
	testsuites.set("time", "0")
	testsuitescomment = "Generated using " + __file__ + " on " + str(datetime.now())
	testsuitescomment = Comment(testsuitescomment)
	testsuites.append(testsuitescomment)
	if verbose:
		print(prettify(testsuites))
	try:
		with open(filename, "w") as fout:
			fout.write(prettify(testsuites))
	except:
		print("File error occured during open for write")
		sys.exit(2)
	return

def createJunitTestsuite(filename, testsuitename, verbose):
	"""Create a JUnit testsuite element - not finished
	"""
	if verbose:
		print("Adding testsuite")

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
		#print(datetime.now().replace(microsecond=0).isoformat())
		child.set("timestamp", timenow)
		xmlRoot.append(child)
		# find element and add attribute
		#print("Ranking")
		#rank = xmlRoot.iter("testsuite")
		#rank.set("name", name)
		#print("Finished")
		#sub = ET.SubElement(xmlRoot, "testsuite")
		#sub.set("name", name)
		tree.write(filename, xml_declaration=True, encoding='utf-8')
	except:
		#print(ET.ParseError)
		print("File error occured during modifying XML")
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

