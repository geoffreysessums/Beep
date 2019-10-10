#! /usr/bin/python
# Program beepDriver.py by Geoffrey Sessums
# Purpose:
#    The program is passed the name of the BEEP source code file. It reads and
#    prints all the BEEP source code lines (showing line numbers) and places
#    them in a list. Finally, it executes the BEEP statements.
# Input:
#    The program is passed the name of the file as a command argument:
#        Example: python3 beepDriver.py inputFile.txt
#    Optionally the program my be passed a -v switch which causes the execution
#    to be verbose:
#        Example: python3 beepDriver.py inputFile.txt -v
# Output:
#    Prints the BEEP source code within the input file along with a line number
#    Prints a sorted list of variables found with the BEEP source code
#    Prints a sorted list of labels found within the BEEP source code
#    Prints an error message if duplicate labels are encountered
#    Prints a statement indicating where execution begins
#    Optionally prints the line number followed by the executing BEEP statement
#     when in verbose mode


# Import sys to obtain command arguments
import sys

# Import Regular Expression for pattern matching
import re

# Import os module for checking file existence, type, and size
import os.path
import os

# Import driver functions
from beepDict import addLabel, printLabels, printVariables, declareVar
from beepExec import execute

# Variables 
labelD = {}
varTypeD = {}
varValueD = {}
lineM = [] 
count = 0
switch = ""

# Print usage message and exit program, if less than 2 command arguments
if len(sys.argv) < 2:
    print("Usage: python3 beepDriver.py inputFile")
    sys.exit(1)

# Check for optional -v flag
if len(sys.argv) == 3:
    switch = sys.argv[2]
    if (switch != "-v"):
        print("Unkown Flag: %s" % (switch))
        sys.exit(1)

# Verify that file exists
if os.path.isfile(sys.argv[1]) == False:
    print("FILE EXISTENCE ERROR: " + sys.argv[1])
    sys.exit(1)

# Open input file for reading
file = open(sys.argv[1], "r", encoding='latin-1')

# Print header
print("BEEP source code in " + sys.argv[1] + ":")

# Read lines of text from the input file
while True:
    inputLine = file.readline()

    # check for no input (i.e. EOF)
    if inputLine == "":
        break
    count = count + 1
    inputLine = inputLine.rstrip('\n')  # remove the newline

    # Tokenize input line
    tokenM = inputLine.split()
    # If token array is empty (blank line), then skip it
    if tokenM != []:
        token = tokenM[0]

    # If the first token is a label, then add label and count to dictionary
    if token[-1] == ':':
        # Strip the colon and make uppercase
        token = token.rstrip(':')
        addLabel(labelD, token, count)

    # If the first token is "VAR", then declare a variable
    if token == "VAR":
        declareVar(tokenM[1:], varTypeD, varValueD)

    # Print Beep source code with line numbers
    print(str(count).rjust(3) + ". " + inputLine)

    lineM.append(inputLine)

# Close file
file.close()

# Print list of variables
print("Variables:")
print("    %-12s %-9s %s" % ("Variable", "Type", "Value"))
printVariables(varTypeD, varValueD)

# Print list of labels
print("Labels:")
print("    %-12s %s" % ("Label", "Statement"))
printLabels(labelD)

execute(lineM, labelD, varTypeD, varValueD, switch)
