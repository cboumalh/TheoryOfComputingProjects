#!/usr/bin/python3

#Team Name: ElSolver
#Team Member: Christopher Boumalhab
#Theory of Computing Project 1, Fall 2022

import sys
import time

# Globals Vars
nbrWffsInFile = 0
nbrSatisWffs = 0
nbrUnsatisWffs = 0
nbrAnswersprov = 0
nbrAnswersCorr = 0
resultFile = 'brute-out.csv'
teamName = 'Elsolver'

# Input Function
# A function which reads in the next wff from a specified input file.
def processFile(filename):

    filePointer = open(filename, "r")

    #Reading the whole file
    while True:

        # Reading Comment Line
        currLine = filePointer.readline().split(' ')
        if currLine[0] == '':
            break

        probNumber = int(currLine[1])
        maxNbrLiteralsInClause = int(currLine[2])


        # Checking whether file gives us the answer
        satis = currLine[3].rstrip().lstrip()

        #Problem Line
        currLine = filePointer.readline().split(' ')
        nbrVars = int(currLine[2])
        nbrClauses = int(currLine[3].rstrip())

        # Meaning they gave us the answer
        if satis != '?':
            global nbrAnswersprov
            nbrAnswersprov += 1
        
        global nbrWffsInFile
        nbrWffsInFile += 1

        # Reading in Clauses
        clauses = []
        nbrLiterals = 0
        for i in range(nbrClauses):
            currLine = filePointer.readline().split(',')
            currLine = currLine[:-1] #we don't want the zero at the end
            nbrLiterals += len(currLine)
            clauses.append(list(map(int, currLine)))

        # Loop through possible assignments and check the result
        isSatisfiable = False
        startTime = time.time() * (10**6)
        solutionComb = ''
        for comb in nextPossAssignment(nbrVars):
            if verifyPossAssignment(clauses, comb) == True:
                solutionComb = comb
                isSatisfiable = True
                break
        endTime = time.time() * (10**6)
        runTime = endTime - startTime

        if isSatisfiable:
            global nbrSatisWffs
            nbrSatisWffs += 1
            isSatisfiable = 'S'
        else:
            global nbrUnsatisWffs
            isSatisfiable = 'U'
            nbrUnsatisWffs += 1

        if satis == isSatisfiable:
            satis = 1
            global nbrAnswersCorr
            nbrAnswersCorr +=1
        elif satis == "?":
            satis = 0
        else:
            satis = -1
    
        printOutput(probNumber, nbrVars, nbrClauses, maxNbrLiteralsInClause,
                nbrLiterals, isSatisfiable, satis, runTime, solutionComb)

    filePointer.close()

# Create Next Possible Assignment function for a certain number of inputs
def nextPossAssignment(nbrVars):
    for iter in range(pow(2, nbrVars)):
        comb = map(int, list(str(bin(iter))[2:].zfill(nbrVars))) #creating a possible combination such as [0,0,0] using binary nbrs
        yield list(comb)


def verifyPossAssignment(clauses, assignment):

    for clause in clauses:
        clauseTruthiness = False
        i = 0

        while i < len(clause):
            currBoolAssignment = bool(int(assignment[abs(clause[i]) - 1]))
            
            # Checking whether a negation exists
            if clause[i] < 0:
                currBoolAssignment = not currBoolAssignment
            
            # We need one literal to be true to make whole clause true
            if currBoolAssignment:
                clauseTruthiness = True
                break

            i += 1

        # One clause false = WHOLE thing false
        if not clauseTruthiness:
            return False
        
    return True

def printOutput(probNumber, nbrVars, nbrClauses, maxNbrLiteralsInClause, nbrLiterals, predictedSAT, answerSAT, runTime, assignment):
    outputList = [probNumber, nbrVars, nbrClauses, maxNbrLiteralsInClause, nbrLiterals, predictedSAT, answerSAT]

    outputList.append(f'{runTime:.1f}')
    # If an assignment exists, add that to list as well
    if predictedSAT == 'S':
        for bit in assignment:
            outputList.append(bit)

    outputList = list(map(str, outputList))

    with open(resultFile, 'a') as of:
        of.write(','.join(outputList))
        of.write('\n')


# Main Execution
def main():
    
    # Parsing command line arguments
    filename = sys.argv[1]

    # Reading in file and performing computations
    processFile(filename)

    # Printing last line
    outputList = [filename.split('.')[0], teamName, nbrWffsInFile, nbrSatisWffs,
                    nbrUnsatisWffs, nbrAnswersprov, nbrAnswersCorr]

    outputList = list(map(str, outputList))
    
    with open(resultFile, 'a') as of:
        of.write(','.join(outputList))


if __name__ == '__main__':
    main()
    