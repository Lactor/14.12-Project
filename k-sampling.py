import election_result as election
import numpy as np
import itertools
import math
import copy

gvoters = []
gvoters.append([0.0/6.0, [0,1,2]])
gvoters.append([0.0/6.0, [0,2,1]])
gvoters.append([0.0/6.0, [1,0,2]])
gvoters.append([0.0/6.0, [1,2,0]])
gvoters.append([6.0/6.0, [2,0,1]])
gvoters.append([0.0/6.0, [2,1,0]])

"""
class FeasibleSpace:
    
    def __init__(self,N):
        self.indices = set()
        currentdistribution = [0 for i in range(N)]
        self.makeIndicesSet(self.indices,currentdistribution,N,0)
        self.points = dict.fromkeys(self.indices,None)

    #NOTE: modifies indices in place
    def makeIndicesSet(self,indices,currentdistribution,N,i):
        if i==(N-1):
            currentdistribution[i] = round(1-sum(currentdistribution[:i]),2)
            indices.add(tuple(currentdistribution))
        else:
            for k in range(int(10*(1-sum(currentdistribution[:i]))+0.0001) + 1):
                currentdistribution[i] = round(float(k)/10,2)
                self.makeIndicesSet(indices,currentdistribution,N,i+1)
        return indices

    def setPoint(self,indices,ishonest):
        point = tuple(indices)
        if point in self.points:
            self.points[point] = ishonest
        else:
            print point, "was not in the reachable range!"
    
    def getPoint(self,indices):
        point = tuple(indices)
        if point in self.points:
            if self.points[point] == None:
                #print point, "was never set during the recursion!"
                return None
            else:
                return self.points[point]
        else:
            print point, "was not in the reachable range!"

    def printAllPointResults(self):
        pointsSorted = []
        for point in self.indices:
            pointsSorted.append(point)
        pointsSorted.sort()
        results = ""
        for point in pointsSorted:
            results += str(point) + " "  +str(self.getPoint(point)) + "\n"
        return results

    def __str__(self):
        return self.printAllPointResults()
"""

def checkPoint(N,S,voters, flag=False):
    if flag:
        print "VOTERS BEFORE", voters
    #Check for all voters
    for voter in voters:
        if flag:
            print "AT VOTER", voter, "VOTERS",voters
        #Find original payoff
        originalPrefs = voter[1]
        honestPayoff = payoff(originalPrefs, election.election_res(N,S,voters))
        
        #Check all possible permutations
        for permutedPref in itertools.permutations(originalPrefs):
            voter[1] = permutedPref
            if payoff(originalPrefs, election.election_res(N,S,voters)) > honestPayoff:
                return False
        #Reset the voter preferences for the next guy
        voter[1] = originalPrefs

    if flag:
        print "VOTERS AFTER", voters
    #Point is good
    return True

def payoff(voterPreferences, elected):
    utility = 0
    for candidate in elected:
        if candidate in voterPreferences:
            utility += len(voterPreferences) - voterPreferences.index(candidate)
    return utility

def explorePointSpace(N,S,voters):
    allPoints = FeasibleSpace(math.factorial(N))
    explorePointSpaceHelper(N,S,voters,allPoints,0)
    return allPoints

def explorePointSpaceHelper(N,S,voters,allPoints,currentVoter):
    originalPref = voters[currentVoter][0]
    voters[currentVoter][0] = 0
    if currentVoter == len(voters)-1:
        before = [voters[i][0] for i in xrange(len(voters))]
        voters[currentVoter][0] = round(1 - reduce(lambda x,y: x+y[0],voters,0),2)
        #print "Checking", [voters[i][0] for i in xrange(len(voters))]
        #tempvoters = copy.deepcopy(voters)
        if checkPoint(N,S,voters):
            allPoints.setPoint([voters[i][0] for i in xrange(len(voters))],True)
            print tuple([voters[i][0] for i in xrange(len(voters))]),True
        else:
            allPoints.setPoint([voters[i][0] for i in xrange(len(voters))],False)
            print tuple([voters[i][0] for i in xrange(len(voters))]),False
    else:
        #print "At voter", currentVoter+1, "with distribution", [voters[i][0] for i in xrange(len(voters))]
        remainder = round(1-reduce(lambda x,y: x+y[0],voters[:currentVoter],0),2)
        for pref in xrange(int(10*remainder) + 1):
            voters[currentVoter][0] = round(float(pref)/10,2)
            explorePointSpaceHelper(N,S,voters,allPoints,currentVoter+1)
    voters[currentVoter][0] = originalPref
    return
        

if __name__=="__main__":

    """          
    voters = []
    voters.append([9.0/26.0, [0,3,1,2]])
    voters.append([6.0/26.0, [1,2,3,0]])
    voters.append([2.0/26.0, [2,1,3,0]])
    voters.append([4.0/26.0, [2,3,1,0]])
    voters.append([5.0/26.0, [3,1,2,0]])

    print checkPoint(4,2,voters)
    """
    
    testAllPoints = FeasibleSpace(24)
    print testAllPoints
    

    """
    voters = []
    voters.append([0.0/6.0, [0,1,2]])
    voters.append([0.0/6.0, [0,2,1]])
    voters.append([0.0/6.0, [1,0,2]])
    voters.append([6.0/6.0, [1,2,0]])
    voters.append([0.0/6.0, [2,0,1]])
    voters.append([0.0/6.0, [2,1,0]])

    
    print explorePointSpace(3,1,voters)
    """

    """
    N = 4
    voters = []
    preferences = [i for i in range(N)]
    proportion = 1.0/math.factorial(N)
    for permutation in itertools.permutations(preferences):
        voters.append([proportion,permutation])
    print voters

    print explorePointSpace(N,1,voters)
    """


    

    
