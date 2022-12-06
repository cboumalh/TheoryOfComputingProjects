#!/usr/bin/python3

#Team Name: TMseason
#Team Member: Christopher Boumalhab
#Theory of Computing Project 3, Fall 2022
import sys
import re

#Parse the data
def getTM(file):
	transitions={}
	nbr = {}
	numTransitions = 0
	fd =  open(file,'r') 
	for line in fd:
		#read lines one by one:	
		if(line[0] == 'A'):
			#Get the alphabet. 
			alpha = []
			alpha = re.split(',|\n', line[2:-1])
			if len(alpha) == 1 and alpha[0] == "":
				return -1
		
			nbr['alphabet'] = alpha
		elif(line[0] == 'Z'):
			#Get the tape alphabet. 
			talpha = []
			talpha = re.split(',|\n', line[2:-1])
			if len(talpha) == 1 and talpha[0] == "":
				return -1
			nbr['talphabet'] = talpha

		elif(line[0] == 'Q'):
			#Get the states:
			states = []
			states = re.split(',|\n', line[2:-1])
			if len(states) == 1 and states[0] == "":
				return -1

			nbr['states'] = states


		elif(line[0] == 'T'):
			#Increase the number of transitions by one:
			numTransitions+=1
	
			#Place the transition function inside a list
			# t[0] is the starting point
			# t[1] is the input
			# t[2] is the next state
			# t[3] is the value to be written
			# t[4] is the direction to go
			t = []
			t = re.split(',|\n', line[2:-1])
			for key,value in transitions.items():
				if value[0] == t[0] and value[1] == t[1]:
					return -3
			if len(t) == 1 and t[0] == "":
				return -1
			elif t[0] not in nbr['states'] or t[2] not in nbr['states']:
				return -1	
			elif t[1] not in nbr['talphabet']:
				return -1
			elif t[3] not in nbr['talphabet']:
				return -1
			elif t[4] is not 'R' and t[4] is not 'L':
				return -2

			transitions[numTransitions] = t

		
		elif(line[0] == 'S'):
			#Obtain the starting state:
			s = []
			s = re.split(',|\n', line[2:-1])
			if len(s) == 1 and s[0] == "":
				return -1

			nbr['start'] = s


		elif(line[0] == 'F'):
			#Obtain the end states:
			f = []
			f = re.split(',|\n', line[2:7])
			if len(f) == 1 and f[0] == "":
				return -1
			elif len(f) is not 2:
				return -1

			nbr['endStates'] = f
		else:
			return -1
	fd.close()
	nbr['transitions'] = transitions
	return nbr



#Function to write down the current state of the Turing machine
def printState(tape,pos,currentState):
	if pos is 0:
		sys.stdout.write('()')
		sys.stdout.write("%s(" % currentState)
		for i in range(pos,len(tape)):
			if i is len(tape)-1:
				sys.stdout.write("%s" % tape[i])
			else:
				sys.stdout.write("%s," % tape[i])
		print(")")
	else: 
		sys.stdout.write('(')
		for i in range(0,pos):
			if i is pos-1:
				sys.stdout.write("%s" % tape[i])
			else:
				sys.stdout.write("%s," % tape[i])
		sys.stdout.write(')')
		sys.stdout.write("%s(" % currentState)
		for i in range(pos,len(tape)):
			if tape[i] is not ' ':
				if i is len(tape)-1:
					sys.stdout.write("%s" % tape[i])
				else:
					sys.stdout.write("%s," % tape[i])
		print(")")



#Tells if the tape input is valid given the alphabet
def inalpha(tm,tape):
	for input in tape:
		if input not in tm['alphabet']:
			print("REJECT: Input not in input alphabet!")
			return 0
	return 1


#Check if the machine is accepting or rejecting: 
def checkIfOver(i,cs,tm,tape,pos,num):
	if cs == tm['endStates'][0]:
		printState(tape,pos,cs)
		print("ACCEPT")
		if i is not num-1:
			print("\n")
		return 1
	elif cs == tm['endStates'][1]:
		printState(tape,pos,cs)
		print("REJECT")
		if i is not num-1:
			print("\n")
		return 1
	return 0


def checkTrans(tm,currentState,tape,pos):
	reject = 1
	for key,value in tm['transitions'].items():
		#If the currentState matches the state from a transition AND the input matches
		if currentState == value[0] and tape[pos] == value[1]:

			reject = 0
			printState(tape,pos,currentState) #print the state
			currentState = value[2]	#Next state
			output = value[3]#Output	
			dir = value[4]	#direction to go

			#If you're moving right on the tape: 
			if dir is "R":
				tape[pos] = output
				pos = pos + 1
				if pos is len(tape):
					tape.append(' ')

			#If you're moving left: 
			elif dir is "L":
				tape[pos] = output
				pos = pos - 1

	return reject,currentState,tm,tape,pos



#This is the big function that handles the input tapes
def processInput(tm):
	#Get the number of input tapes, with error checking
	numInputTapes = input("")
	if not numInputTapes.isdigit():
		print("Number of inputs needs to be a positive number.")
		return
	else:
		numInputTapes = int(numInputTapes)
		if numInputTapes == 0:
			print("Number of inputs needs to be a positive number.")
			return

	#Get each input tape and delimit it. 
	for i in range(numInputTapes):
		pos = 0
		done = 0
		it = input("")

		#Check and make sure the input is in the alphabet:
		tape = re.split(',',it)
		if not inalpha(tm,tape):
			continue

		#Set the current state to whatever the start state is: 
		currentState = tm['start'][0]
		numSteps = 0

		#for each input character (item), interpret its effect:
		while not done:
			reject = 1
			numSteps = numSteps + 1
			if numSteps == 1000:
				print("DID NOT HALT")
				done = 1
				break

			#Check if it's accepted or not
			done = checkIfOver(i,currentState,tm,tape,pos,numInputTapes)
			if done: 
				break

			#run through the transitions and find the rule that governs the state we are in:
			reject,currentState,tm,tape,pos = checkTrans(tm,currentState,tape,pos)

			#if there is no transition, move to the reject state
			if reject:
				printState(tape,pos,currentState) 	
				pos = pos + 1
				if pos is len(tape):
					tape.append(' ')
				currentState = tm['endStates'][1]

def main(argv):
	#The Turing Machine is described by a dictionary
	tm = {}
	if len(argv) == 2:
		tm = getTM(argv[1])	
	else:
		print("ERROR, USAGE: ./tm.py TMFILE < TM_INPUT")
		sys.exit(0)


	#Error checking
	if(tm == -1):
		print("ERROR, INVALID TM INPUT!")
	elif tm == -3:
		print("ERROR, TM INPUT IS NOT DETERMINISTIC!")
	else:
		if(tm != 0):
			#There is a valid NFA: 
			processInput(tm)



if __name__ == "__main__":
	main(sys.argv)

