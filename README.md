# jurepgen
JUnit Report Generator
======================

jurepgen will be a JUnit test report generator written in Python. Goal is to allow any testing framework for any code to generate JUnit reports that can be displayed using Jenkins.

The purpose of this program is to allow testers to create a JUnit-format XML output that provides testing results from an arbitrary testing procedure.

This program is designed to be called from the command line within Jenkins as a build step. The first call creates the basic 'testsuites' element of the XML file. Each further call adds a testsuite, testcase, and other elements to the file.

The process is as follows:

* python3 jurepgen.py -o "testresults.xml"
** Generates basic JUnit compliant XML file with timestamp
* python3 jurepgen.py -i "testreuslts.xml" -t -n "Test Suite 1"
** Adds "Test Suite 1" testsuite to existing JUnit XML file.

