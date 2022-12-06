#!/usr/bin/python3

#Team Name: NFAeater
#Team Member: Christopher Boumalhab
#Theory of Computing Project 2, Fall 2022

import sys
import csv

epsilon = '~'

class NFA:

    def __init__(self, states, alphabet, start, end, transitions):
        self.states = states
        self.alphabet = [x for x in alphabet if x != '']
        self.start = [x for x in start if x != '']
        self.end = [x for x in end if x != '']

        self.transitions = {x:{}  for x in self.states}
        for l in transitions:
            if l[1] in self.transitions[l[0]]:
                self.transitions[l[0]][l[1]].append(l[2])
            else:
                self.transitions[l[0]][l[1]] = [l[2]]


def buildNFA(filename):
    # open file
    with open(filename, "r", newline='', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        next(reader, None)
        reader = list(reader)

        currNFA = NFA(reader[0], reader[1], reader[2], reader[3], reader[4:])

        return currNFA


def tracePaths(currNFA, string):
    allTransitions = []
    theStack = []
 
    for startStates in currNFA.start:
        theStack.append([startStates, string, [startStates]])
    

    while len(theStack) > 0:
        top = theStack.pop()

        if len(top[1]) == 0:
            allTransitions.append(top[2])

            if epsilon in currNFA.transitions[top[0]] and len(top[2]) == 1 and top[2][0] == top[0]:
                for i in range(0, len(currNFA.transitions[top[0]][epsilon])):
                        allTransitions.append([currNFA.transitions[top[0]][epsilon][i]])
            continue

        if top[1][0] in currNFA.transitions[top[0]]:
            for i in range(0, len(currNFA.transitions[top[0]][top[1][0]])):
                theStack.append([currNFA.transitions[top[0]][top[1][0]][i], top[1][1:], top[2] + [currNFA.transitions[top[0]][top[1][0]][i]]])

                child = currNFA.transitions[top[0]][top[1][0]][i]

                if epsilon in currNFA.transitions[child]:
                    for i in range(0, len(currNFA.transitions[child][epsilon])):
                        theStack.append([currNFA.transitions[child][epsilon][i], top[1][1:], top[2] + [currNFA.transitions[child][epsilon][i]]])
        
        if epsilon in currNFA.transitions[top[0]] and len(top[2]) == 1 and top[2][0] in currNFA.start and top[0] in currNFA.start:
            for i in range(0, len(currNFA.transitions[top[0]][epsilon])):
                    theStack.append([currNFA.transitions[top[0]][epsilon][i], top[1], [currNFA.transitions[top[0]][epsilon][i]]])


    return allTransitions


def getFinalStates(possiblePaths, currNFA):
    result = filter(lambda l: l[-1] in currNFA.end, possiblePaths)
    return list(result)
    

# Main Execution
def main():
    
    # Parsing command line arguments
    arguments = sys.argv[1:3]

    if len(arguments) < 2:
        print("First argument should be CSV file for NFA, second argument should be string entry for NFA (enter '' for empty string)")
        return

    # Reading in file and performing computations
    currNFA = buildNFA(arguments[0])
    possiblePaths = tracePaths(currNFA, arguments[1])
    finalStatePaths = getFinalStates(possiblePaths, currNFA)
    with open(f"{arguments[0].split('.')[0]}_{arguments[1]}_solution.txt", 'w') as f:
        f.write("These are all the possible paths:\n")
        for line in possiblePaths:
            f.write(f"{line}\n")
        
        f.write("These are all the paths that make it to the final state:\n")
        for line in finalStatePaths:
            f.write(f"{line}\n")



if __name__ == '__main__':
    main()