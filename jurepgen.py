#!/usr/bin/python

from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom
from datetime import datetime
import argparse, sys, encodings

def prettify(elem):
	"""Return a pretty-printed XML strong for the Element.
	"""
	rough_string = ElementTree.tostring(elem, "utf-8")
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")

def createJunitReport(testsuitesname):
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
	print(prettify(testsuites))
	return

def main():
	verbose = False
	testsuitesname = ""

	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-i", "--inputfile", help="XML input file name")
	group.add_argument("-o", "--outputfile", help="XML output file name")
	parser.add_argument("-v", "--verbose", help="output status during operation", action="store_true")
	parser.add_argument("-n", "--name", help="testsuites name")
	args = parser.parse_args()

	if args.verbose:
		verbose = True
		print("Verbose Mode")

	if args.name:
		testsuitesname = args.name
		if verbose:
			print("testsuites name is: {}".format(args.name))

	if args.inputfile:
		if verbose:
			print("Input file found: {}".format(args.inputfile))
		sys.exit()

	elif args.outputfile:
		if verbose:
			print("Output file found: {}".format(args.outputfile))
		createJunitReport(testsuitesname)
		sys.exit()

if __name__ == "__main__":
	main()

