#! /usr/bin/python

# Filename: beepDict.py by Geoffrey Sessums
# Purpose:
#     Provides the functions declareVar, printVariables, printLabels, & addLabel

# Function: declareVar
# Purpose:
#    Saves variable names, types, and optional values in the dictionaries:
#        varTypeD, varValueD, typeD, valueD
# Parameters:
#    tokenM - array containing variable name, type, and optional value
#    varTypeD - dictionary containing variable names (keys) and types (values)
#    varValueD - dictionary containing variable names (keys) and values (values)
# Returns:
#    N/A
def declareVar(tokenM, varTypeD, varValueD):
    varTypeD[tokenM[1]] = tokenM[0]
    # If tokenM contains optional value, then save it in value dictionary
    if len(tokenM) == 3 :
        if tokenM[2][0] == '"':
            varValueD[tokenM[1]] = tokenM[2].strip('"')
        else:
            varValueD[tokenM[1]] = tokenM[2]

# Function: printVariables
# Purpose:
#    Print a list of variable names, types, and possibly values 
# Parameters:
#    None 
# Returns:
#    N/A
def printVariables(varTypeD, varValueD):
    for name in sorted(varTypeD):
        # If value for variable (i.e. key) is not found, then print the variable
        # name and type
        if varValueD.get(name, "NF") == "NF":
            print("    %-12s %-9s" % (name.upper(), varTypeD[name]))
        else:
            # Otherwise print variable name, type, and value
            print("    %-12s %-9s %s" % (name.upper(), varTypeD[name], varValueD[name]))

# Function: printLabels
# Purpose:
#   Print a list of labels along with their line number
# Parameters:
#    None 
# Returns:
#    N/A
def printLabels(labelD):
    for label in sorted(labelD):
        print("    %-12s %s" % (label.upper(), labelD[label]))

# Function: addLabel
# Purpose:
#    Add a label to the label dictionary. Print error if the label is a duplicate 
# Parameters:
#    label - label name
#    count - line number of label
# Returns:
#    N/A
def addLabel(labelD, token, count):
    # If label is not found in label dictionary, then add it; otherwise print error
    if labelD.get(token, "NF") == "NF": 
        labelD[token] = count
    else:
        print("***Error: label %s appears on multiple lines: %s and %s" % (token, labelD[token], count))
