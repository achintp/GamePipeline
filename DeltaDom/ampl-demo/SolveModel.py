import sys
import Game
import pprint
import heapq
from subprocess import call


def solveModel(runFile):
	call(["./ampl", runFile])
	try:
		with open('delta.out','r') as inFile:
			delta = inFile.readline()
	except:
		print "Out file not printed"

	return delta

def deltaElim(game, delta=None, size=None):
	acumDelta = 0
	leastDelta = 9999
	roles = []

	#Strategy to be pruned
	pruneStrategy = None 

	#Keep track of the current count of strats
	strats = {}
	numStrats = {}
	deltas = None

	for role, num in zip(game.roles, game.numStrategies):
		roles.append(role)
		numStrats[role] = num
		strats[role] = list(game.strategies[role])
		# deltas[role] = []
		#pprint.pprint(game.stratInd)

	#Remove strictly dominated for each player
	run = True
	while(run):
		deltas = getDeltas(roles, numStrats, strats, game.payoffMat, game.roleInd, game.stratInd)
		#Find the most minimum delta
		#Deals with finding the strictly dominated strategies
		print deltas

		# if float(deltas[0][0]) > 0:
		# 	print "All deltas are positive"
		# 	run = False
		# else:
		# 	print "Eliminating",deltas[0][0]
		# 	smallest = heapq.heappop(deltas)
		# 	numStrats[smallest[2]] -= 1
		# 	strats[smallest[2]].remove(smallest[1])

		if deltas[0][0] < 0:
			while deltas[0][0] < 0:
				print "Eliminating",deltas[0][0]
				smallest = heapq.heappop(deltas)
				numStrats[smallest[2]] -= 1
				strats[smallest[2]].remove(smallest[1]) 
			print "Removed all negative in this iteration"
		else:
			print "No negative deltas"
			run = False

	#If size constraint has to be met		
	if size == None:
		print "Size contstraint met"
	else:
		while(isGreater(numStrats, size)):
			deltas = getDeltas(roles, numStrats, strats, game.payoffMat, game.roleInd, game.stratInd)
			# print "Eliminating",deltas[0][0]
			#Remove all the ngative deltas that may occur
			if deltas[0][0] < 0:
				while deltas[0][0] < 0:
					print "Eliminating negative-",deltas[0][0]
					smallest = heapq.heappop(deltas)
					numStrats[smallest[2]] -= 1
					strats[smallest[2]].remove(smallest[1]) 
				print "Removed all negative in this size iteration"
			if(isGreater(numStrats, size)):
				print "Removing positive delta-", deltas[0][0]
				smallest = heapq.heappop(deltas)
				acumDelta += smallest[0]
				numStrats[smallest[2]] -= 1
				strats[smallest[2]].remove(smallest[1])
		#print deltas
	print "Cumulative Delta - " + str(acumDelta)
	printStrategies(strats)
	return

#Tests whether the size criteria has been met
def isGreater(numStrats, size):
	ans = True
	for k,v in numStrats.iteritems():
		if k == 'ATT' and v <= size:
			ans = False
	return ans

#Write - need to interface with refactor method of Game.py
def returnParams(game, strats, numStrats):
	redMat = [[(None, None) for j in range(numStrats[game.roles[1]])]\
		for i in range(numStrats[game.roles[0]])]	
	return

def printStrategies(strats):
	for k,v in strats.iteritems():
		print k
		pprint.pprint(v)

#All this function is going to do is get the deltas
#No need to complicate it
def getDeltas(roles, nums, strats, payoffs, roleInd, stratInd):
	debug = 1
	deltas = []
	debugCounter = 0

	for item in zip(roles, roles[1:]+roles[:1]):
		#Get the different roles
		curRole = item[0]
		otherRole = item[1]

		if debug:
			print curRole, otherRole

		#Identify different strategies
		curStrats = []
		otherStrats = []
		for item in strats[curRole]:
			curStrats.append(stratInd[curRole][item])
		for item in strats[otherRole]:
			otherStrats.append(stratInd[otherRole][item])

		if debug:
			print curStrats
			print otherStrats
		
		#Get current role index
		curInd = None
		for k,v in roleInd.iteritems():
			if v == curRole:
				curInd = k
		print curInd

		#prepare deltas
		# deltas[curRole] = []
		for item in curStrats:
			#Print the data file
			with open('deltaD.data','w') as df:
				df.write('set Strategy1 :=')
				for strat in otherStrats:
					df.write( " "+str(strat))
				df.write(';\n')
				df.write('set Strategy2 := ')
				for strat in curStrats:
					if strat != item:
						df.write(" "+str(strat))
				df.write(';\n')
				df.write('set T := ' + str(item) + ';\n')
				df.write('param u\n')
				#print the matrix
				for i in curStrats:
					for j in otherStrats:
						df.write('['+str(i)+','+str(j)+'] ')
						#Make sure you index properly
						if curInd == 0:
							df.write(str(payoffs[i][j][curInd]))
						if curInd == 1:
							df.write(str(payoffs[j][i][curInd]))
						df.write(' ')
				df.write(';')
				debugCounter += 1
			# deltas[curRole][item] = solveModel('deltaRun.run')
			curStrat = None
			for k,v in stratInd[curRole].iteritems():
				if v == item:
					curStrat = k
			heapq.heappush(deltas, (float(solveModel('deltaRun.run')), curStrat, curRole))
	# pprint.pprint(deltas)
	return deltas

if __name__ == '__main__':
	print solveModel(sys.argv[1])