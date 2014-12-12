
import numpy as np
import copy

def spread_votes(cand, voters, votes, votes_cor, in_race, threshold):
    # ratio that tells us how to divide the remainding of the votes
    
    #print "Spreading votes from ", cand
    
    leftover = votes[cand] - threshold
    initial_vote = votes[cand]
    #print votes[cand]
    #print threshold
    #print leftover
    disregarded = 0.0

    if initial_vote == 0.0:
        return (voters, votes, votes_cor)
    
    temp_list = copy.deepcopy(votes_cor[cand])
    for vote_ref in temp_list:
        #print vote_ref
        #print voters[vote_ref[0]][1]
        #print initial_vote
        passing = leftover * voters[vote_ref[0]][0]/initial_vote
        voters[vote_ref[0]][0] -= passing
        #print votes[cand]
        votes[cand] -= passing
        #print votes[cand]
        #print passing
        #print votes
        #print  voters[vote_ref[0]][1][vote_ref[1] +1 : ]
        temp_voter = [ passing, voters[vote_ref[0]][1][vote_ref[1] +1 : ]]
        #print temp_voter

        if len(temp_voter[1]) == 0:
            # discard votes
            disregarded += temp_voter[0]
        
        else:
            index =1
            next_vote = temp_voter[1][0]
            #print "NEXT_VOTE: ",next_vote
            while index < len(temp_voter[1]) and in_race[next_vote] == 0:
                next_vote = temp_voter[1][index]
                index += 1
            
            if index == len(temp_voter[1]) and not in_race[next_vote]:
                #print "disregard"
                disregarded+= temp_voter[0]
            else:
                #print "ADDIND"
                voters.append(temp_voter)
                #print cand
                #print next_vote
                votes_cor[next_vote].append([next_vote, index-1])
                votes[next_vote] += temp_voter[0]
                #print votes
                #print temp_voter[0]

    if disregarded > 0:
        new_threshold = threshold * 1.0/(1.0-disregarded)
        #print "Spread"
        for i in range(len(votes)):
            if votes[i] > new_threshold:
                voters, votes, votes_cor = spread_votes( i, voters, votes, votes_cor, in_race, new_threshold)
                break
                

    return (voters, votes,votes_cor)


def election_res(N, S, voters): 
# voters must correspond to a list of tuples,
# first value is fraction of the population to whom the votes correspond to
# and a list with the ranking of the candidates zero-counted
    voters = copy.deepcopy(voters)
    
    assert(N>=S)

    votes = np.zeros(N)
    votes_cor = []
    for i in range(N):
        votes_cor.append([])

    #Initial count of votes
    for i in range(len(voters)):
        votes[voters[i][1][0]] += voters[i][0]
        votes_cor[voters[i][1][0]].append([i,0])

    threshold = 1.0/(S+1)



    seated = []
    in_race = [True]*N

    while len(seated) < S:
        # While we don't have enough seated members
        #print 
        #print 
        #print "Potato"
        #su = 0

        #for k in voters:
        #    print k
        #    su += k[0]
        #print su
            
        #print threshold
        #print votes
        
        changed = False

        #Check votes for winners
        for i in range(N):
            if in_race[i] == True and votes[i] >= threshold:
                seated.append(i)
                in_race[i] = False
                if len(seated) == S:
                    return seated
                    
                voters, votes,votes_cor = spread_votes(i, voters, votes, votes_cor, in_race, threshold)
                changed= True
        #print "Changed: ", changed


        # check for the candidate with the lowest votes
        #print "POTATO"
        #print votes_cor
        #print votes
        minv = 1000
        minc = -1
        for i in range(N):
            if in_race[i] == 1 and votes[i] < minv:
                minc = i
                minv = votes[i]
        #print "Dropping candidate: ", minc
        voters, votes,votes_cor = spread_votes(minc, voters, votes, votes_cor,in_race,  0.0)
        #print votes


        
if __name__=="__main__":    
    voters = []
    voters.append([9.0/26.0, [0,3,1,2]])
    voters.append([6.0/26.0, [2,3,1,0]])
    voters.append([2.0/26.0, [2,3,1,0]])
    voters.append([4.0/26.0, [3,1,2,0]])
    voters.append([5.0/26.0, [1,2,3,0]])

    print election_res(4,2, voters)

    voters = []
    voters.append([9.0/26.0, [0]])
    voters.append([6.0/26.0, [2,3,1]])
    voters.append([2.0/26.0, [3,2,1]])
    voters.append([4.0/26.0, [3,1,2]])
    voters.append([5.0/26.0, [1,2,3]])

    print election_res(4,2, voters)

    voters = []
    voters.append([9.0/26.0, [0,3,1,2]])
    voters.append([6.0/26.0, [1,2,3,0]])
    voters.append([2.0/26.0, [2,1,3,0]])
    voters.append([4.0/26.0, [2,3,1,0]])
    voters.append([5.0/26.0, [3,1,2,0]])

    print election_res(4,2, voters)
