#! /usr/bin/python

# Filename: beepExec.py by Geoffrey Sessums

# Purpose:
#     Provides functions that execute BEEP source code.
# Usage:
#     python3 beepDriver.py beepInput.txt 
#     python3 beepDriver.py beepInput.txt -v
# Input:
#     lineM - array of lines read from BEEP source code.
#     labelD - dictionary containing label names (keys) and line numbers (values)
#     varTypeD - dictionary containing variable names (keys) and types (values)
#     varValueD - dictionary containing variable names (keys) and values (values)
#     switch - optional flag indicating verbose printing for debugging
# Output:
#     In defalut mode (i.e. without optional -v) prints BEEP print commands
#     In verbose mode prints every line executed with corresponding line numbers
#     Prints the following exceptions:
#         TooFewOperands – the various operations were given too few operands 
#             (e.g., only one operand for a greater than)
#         VarNotDefined – a referenced variable is not defined
#         LabelNotDefined – a referenced label is not defined
#         InvalidExpression – other problems with expressions such as unknown 
#             operator
#         InvalidValueType – an operation expecting an INT had a value which 
#             was of the wrong type

class TooFewOperands(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class VarNotDefined(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class LabelNotDefined(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class InvalidExpression(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class InvalidValueType(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

# Function: execute(lineM, labelD, varTypeD, varValueD, switch)
# Purpose: 
#     Executes BEEP soure code
# Parameters:
#     lineM - array of lines read from BEEP source code.
#     labelD - dictionary containing label names (keys) and line numbers (values)
#     varTypeD - dictionary containing variable names (keys) and types (values)
#     varValueD - dictionary containing variable names (keys) and values (values)
#     switch - optional flag indicating verbose printing for debugging
# Returns:
#     N/A
def execute(lineM, labelD, varTypeD, varValueD, switch):
    # Execute BEEP source code
    print("execution begins...")

    lineNum = 0    # current line executed
    counter = 0    # total of lines executed 
    # Loop through lineM containing lines of BEEP source code
    while lineNum < len(lineM):
        counter = counter + 1

        # Tokenize input line
        tokenM = lineM[lineNum].split()

        # Limit line execution to 5,000 
        if (counter + 1) > 5000:
            print("***Error: an infinite loop was most likely encountered")
            break
        # Print line number and line currently executing
        if switch == "-v":
            print("executing line %d: %s" % (lineNum + 1, lineM[lineNum]))
        
        # If token array is empty (blank line), then skip it
        if tokenM == []:
            lineNum = lineNum + 1
            continue
        token = tokenM[0]

        # If the first token is a label, then process following statement 
        if token[-1] == ':':
            token = tokenM[1]
            tokenM = tokenM[1:]
            #print(token)
            #print(tokenM)
        try: 
            # Perform ASSIGN statement
            if token == "ASSIGN":
                # get variable name
                varNm = tokenM[1]
                # get expression
                exprM = tokenM[2:]
                execAssign(varNm, exprM, varTypeD, varValueD)

            # Process IF statement
            if token.upper() == "IF":
                # get expression
                exprM = tokenM[1:-1]
                # get label which is the always last element of tokenM
                label = tokenM[-1]
                lineNum = execIf(exprM, label, labelD, varTypeD, varValueD, lineNum)
                continue

            # Process GOTO statement
            if token == "GOTO":
                # get label
                label = tokenM[1]
                lineNum = execGoTo(label, labelD)
                continue

            # Get PRINT statement
            if token == "PRINT":
                # pass varLiteral1 varLiteral2 ... varLiteralN
                execPrint(tokenM[1:], varTypeD, varValueD)
    
        except(InvalidValueType, TooFewOperands, VarNotDefined, LabelNotDefined, InvalidExpression) as e:
            print ("*** line %d error detected ***" % (lineNum+1))
            print("%-10s %d *** %s ***" % (" ", lineNum+1, str(e.args[1])))
            break
        except Exception as e:
            print("*** line %d error detected ***" % (lineNum+1))
            print(e)
            break
        except:
            print("*** line %d error detected ***" % (lineNum+1))
            traceback.print_exc()
            break
        lineNum = lineNum + 1
    # Print total number of lines executed
    print("execution ends, %d lines executed" % (counter))

# Function: execAssign
# Purpose: 
#   Assigns the value of the expression to the specified variable which must
#   have been declared.  
# Parameters: 
#    varNm- name of variable 
#    exprM - list of expression elements which is one of:
#        varLiteral	           return the string value (without the ") for a string 
#                                  literal, the value of a numeric constant or return the 
#                                  value of a variable
#        * varLiteral varNumber	   return a string with varLiteral replicated varNumber times
#        + varNumber1 varNumber2   return the sum of the values
#        - varNumber1 varNumber2   return the difference of the values (varNumber1 minus varNumber2)
#        > varNumber1 varNumber2   return True if varNumber1 > varNumber2; this is a numeric comparison
#        >= varNumber1 varNumber2  return True if varNumber1 >= varNumber2; this is a numeric comparison
#        & varLiteral1 varLiteral2 return the concatenation of the two strings
#
#    varTypeD - dictionary containing variable names (keys) and types (values)
#    varValueD - dictionary containing variable names (keys) and values (values)
# Returns:
#    N/A
def execAssign(varNm, exprM, varTypeD, varValueD):
    # Is varNm defined?
    if varTypeD.get(varNm, "NF") == "NF":
        raise VarNotDefined("variable %s is not defined" % (varNm))
    varValueD[varNm] = evalExpr(exprM, varTypeD, varValueD)

# Function: execIf
# Purpose:
#     Executes BEEP if statements
# Parameters:
#    exprM - list of expression elements which is one of:
#        varLiteral	           return the string value (without the ") for a string 
#                                  literal, the value of a numeric constant or return the 
#                                  value of a variable
#        * varLiteral varNumber	   return a string with varLiteral replicated varNumber times
#        + varNumber1 varNumber2   return the sum of the values
#        - varNumber1 varNumber2   return the difference of the values (varNumber1 minus varNumber2)
#        > varNumber1 varNumber2   return True if varNumber1 > varNumber2; this is a numeric comparison
#        >= varNumber1 varNumber2  return True if varNumber1 >= varNumber2; this is a numeric comparison
#        & varLiteral1 varLiteral2 return the concatenation of the two strings
#    label - label name
#    label - dictionary containing label names (keys) and line numbers (values)
#    varTypeD - dictionary containing variable names (keys) and types (values)
#    varValueD - dictionary containing variable names (keys) and values (values)
#    lineNum - current line of execution
# Returns:
#    Line number of a label if jump is necessary
#    Current line number if jump is unnecessary
def execIf(exprM, label, labelD, varTypeD, varValueD, lineNum):
    boolean = evalExpr(exprM, varTypeD, varValueD)
    # If condition is true perform a goto
    if boolean == True:
        return  execGoTo(label, labelD)
    return lineNum + 1

# Function: execPrint
# Purpose:
#    Execute print statements
# Parameters:
#    tokenM - list containing line tokens
#    varTypeD - dictionary containing variable names (keys) and types (values)
#    varValueD - dictionary containing variable names (keys) and values (values)
# Returns:
#    N/A
def execPrint(tokenM, varTypeD, varValueD):
    for token in tokenM: 
        var = evalVar(token, varTypeD, varValueD) 
        print(var, end=" ")
    print()

# Function: execGoTo
# Purpose:
#    Execute goto statements
# Parameters:
#    label - label name 
#    label - dictionary containing label names (keys) and line numbers (values)
# Returns:
#    Line number where the label is located
def execGoTo(label, labelD):
    if labelD.get(label, "NF") == "NF":
        raise LabelNotDefined("label '%s' is not defined" % (label))
    return labelD[label] - 1

# Function: evalExpr
# Purpose:
#    Evaluates expressions
# Parameters:
#    exprM - list of expression elements which is one of:
#        varLiteral	           return the string value (without the ") for a string 
#                                  literal, the value of a numeric constant or return the 
#                                  value of a variable
#        * varLiteral varNumber	   return a string with varLiteral replicated varNumber times
#        + varNumber1 varNumber2   return the sum of the values
#        - varNumber1 varNumber2   return the difference of the values (varNumber1 minus varNumber2)
#        > varNumber1 varNumber2   return True if varNumber1 > varNumber2; this is a numeric comparison
#        >= varNumber1 varNumber2  return True if varNumber1 >= varNumber2; this is a numeric comparison
#        & varLiteral1 varLiteral2 return the concatenation of the two strings
#    varTypeD - dictionary containing variable names (keys) and types (values)
#    varValueD - dictionary containing variable names (keys) and values (values)
# Returns:
#    Evaluated value of expression
def evalExpr(exprM, varTypeD, varValueD):
    # Evaluate single item expression
    if len(exprM) == 1:
        return evalVar(exprM[0], varTypeD, varValueD)
    # Evaluate three item expressions by first getting operands
    elif len(exprM) != 3:
        raise TooFewOperands("expression '%s' has too few operands" % (exprM))
    op1 = evalVar(exprM[1], varTypeD, varValueD)
    op2 = evalVar(exprM[2], varTypeD, varValueD)
    # Evaluate prefixed operator
    if exprM[0] == '>':
        return evalGreater(op1, op2)
    if exprM[0] == ">=":
        return evalGreaterEq(op1, op2)
    if exprM[0] == '&':
        return evalCat(op1, op2)
    if exprM[0] == '*':
        return evalRep(op1, op2)
    if exprM[0] == '+':
        return evalAdd(op1, op2)
    if exprM[0] == '-':
        return evalSub(op1, op2)
    else:
        raise InvalidExpression("unknown operator: %s " % (exprM[0]))

# Function: evalGreater
# Purpose:
#    Evaluate a greater than expression
# Parameters:
#    op1 - first operand
#    op2 - second operand
# Returns:
#    True if op1 is greater than op2
#    False if op1 is NOT greater than op2
def evalGreater(op1, op2):
    try:
        iVal1 = int(op1)
    except:
        raise InvalidValueType("'%s' is not numeric" % (op1))
    try:
        iVal2 = int(op2)
    except:
        raise InvalidValueType("'%s' is not numeric" % (op2))
    return iVal1 > iVal2

# Function: evalGreaterEq
# Purpose:
#    Evaluate a greater than or equal expression
# Parameters:
#    op1 - first operand
#    op2 - second operand
# Returns:
#    True if op1 is greater than or equal to op2
#    False if op1 is NOT greater than or equal to op2
def evalGreaterEq(op1, op2):
    try:
        iVal1 = int(op1)
    except:
        raise InvalidValueType("'%s' is not numeric" % (op1))
    try:
        iVal2 = int(op2)
    except:
        raise InvalidValueType("'%s' is not numeric" % (op2))
    return iVal1 >= iVal2

# Function: evalCat
# Purpose:
#    Evaluate concantenation statement
# Parameters:
#    op1 - first operand
#    op2 - second operand
# Returns:
#    The concatenation of two strings
def evalCat(op1, op2):
    try:
        str1 = str(op1)
    except:
        raise InvalidValueType("Operand is not a string")
    try:
        str2 = str(op2)
    except:
        raise InvalidValueType("Operand is not a string")
    return str1 + str2 

# Function: evalRep
# Purpose:
#    Preforms string replication
# Parameters:
#    op1 - first operand
#    op2 - second operand
# Returns:
#    Replicated string
def evalRep(op1, op2):
    try:
        str1 = str(op1)
    except:
        raise InvalidValueType("Operand is not a string")
    try:
        iVal = int(op2)
    except:
        raise InvalidValueType("'%s' is not numeric" % (op2))
    return str1 * iVal

# Function: evalAdd
# Purpose:
#    Performs addition of two operands
# Parameters:
#    op1 - first operand
#    op2 - second operand
# Returns:
#    Sum of two operands
def evalAdd(op1, op2):
    try:
        iVal1 = int(op1)
    except:
        raise InvalidValueType("'%s' is not numeric" % (op1))
    try:
        iVal2 = int(op2)
    except:
        raise InvalidValueType("'%s' is not numeric" % (op2))
    return iVal1 + iVal2

# Function: evalSub
# Purpose:
#    Performs subtraction of two operands
# Parameters:
#    op1 - first operand
#    op2 - second operand
# Returns:
#    Difference of two operands
def evalSub(op1, op2):
    try:
        iVal1 = int(op1)
    except:
        raise InvalidValueType("'%s' is not numeric" % (op1))
    try:
        iVal2 = int(op2)
    except:
        raise InvalidValueType("'%s' is not numeric" % (op2))
    return iVal1 - iVal2

# Function: evalVar
# Purpose:
#    Evaluate a single variable
# Parameters:
#    op - operand is a variable
#    varTypeD - dictionary containing variable names (keys) and types (values)
#    varValueD - dictionary containing variable names (keys) and values (values)
# Returns:
#    Value of the variable
def evalVar(op, varTypeD, varValueD):
    # Return a stripped string
    if op[0] == '"':
        return op[1:-1]
    # Return decimal
    if op.isdecimal():
        return op
    value = varValueD.get(op, "NF")
    # Return evaluated variable if defined
    if value == "NF":
        raise VarNotDefined("variable %s not defined" % (op))
    return value
