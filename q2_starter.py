################################################################################
# Starter code for Problem 2
# Author: poorvib@stanford.edu
# Last Updated: Oct 4, 2017
# Note: This starter code is only one possible implementation for this question.
# Please feel free to implement your own solution and/or modify this code in
# any way that you need.
################################################################################

import snap
import random

# Problem 2.1 Functions
def loadSigns(filename):
    """
    :param - filename: undirected graph with associated edge sign

    return type: dictionary (key = node pair (a,b), value = sign)
    return: Return sign associated with node pairs. Both pairs, (a,b) and (b,a)
    are stored as keys. Self-edges are NOT included.
    """
    signs = {}
    with open(filename, 'r') as ipfile:
        for line in ipfile:
            if line[0] != '#':
                line_arr = line.split()
                if line_arr[0] == line_arr[1]:
                    continue
                node1 = int(line_arr[0])
                node2 = int(line_arr[1])
                sign = int(line_arr[2])
                signs[(node1, node2)] = sign
                signs[(node2, node1)] = sign
    return signs

def computeTriadCounts(G, signs):
    """
    :param - G: graph
    :param - signs: Dictionary of signs (key = node pair (a,b), value = sign)

    return type: List, each position representing count of t0, t1, t2, and t3, respectively.
    return: Return the counts for t0, t1, t2, and t3 triad types. Count each triad
    only once and do not count self edges.
    """

    triad_count = [0, 0, 0, 0] # each position represents count of t0, t1, t2, t3, respectively
    t0, t1, t2, t3= 0, 0, 0, 0   
        
    ############################################################################
    for NI in G.Nodes():
        #print ("signs from", NI.GetId())
        for e1 in range(0, NI.GetDeg()):
            for e2 in range (0, NI.GetDeg()):
                #get triad by looking at neighbors of every node 
                if (e1 != e2):
                    n1 = NI.GetNbrNId(e1)
                    n2 = NI.GetNbrNId(e2)
                    pcount, ncount = 0, 0
                    #print (n1, n2)
                    # Get the triads and count positive and negative edges
                    # counting them will tell us the type of the triad
                    if NI.GetId() != n1 and NI.GetId() != n2 and G.IsEdge(n1, n2) and G.IsEdge(NI.GetId(),n1) and G.IsEdge(NI.GetId(), n2):
                        if (signs[(NI.GetId(), n1)] == 1):
                            pcount += 1
                        else:
                            ncount += 1
                            
                        if (signs[(NI.GetId(), n2)] == 1):
                            pcount += 1
                        else:
                            ncount += 1
                        
                        if (signs[(n1, n2)] == 1):
                            pcount += 1
                        else:
                            ncount += 1

                    if (ncount == 3):
                        t0 += 1
                        
                    elif (ncount == 2):
                        t1 += 1

                    elif (ncount == 1):
                        t2 += 1
                        
                    elif (pcount == 3):
                        t3 += 1
                            
                            
    triad_count = [t0/6, t1/6, t2/6, t3/6]

    ############################################################################

    return triad_count

def displayStats(G, signs):
    '''
    :param - G: graph
    :param - signs: Dictionary of signs (key = node pair (a,b), value = sign)

    Computes and prints the fraction of positive edges and negative edges,
        and the probability of each type of triad.
    '''
    fracPos = 0
    fracNeg = 0
    probs = [0,0,0,0]

    ############################################################################
    # TODO: Your code here! (Note: you may not need both input parameters)
    pos, neg, count = 0, 0, 0
    for key, value in signs.iteritems():
        if value == 1:
            pos += 1
            
        else:
            neg += 1
    
        count += 1

    fracPos = pos / (1.0 * (pos + neg))
    fracNeg = neg / (1.0 * (pos + neg))
    
    p_t0 = fracNeg * fracNeg * fracNeg # (1-p) * (1- p) * (1-p)
    p_t1 = fracPos * fracNeg * fracNeg * 3   # p * (1-p) * (1-p)
    p_t2 = fracPos * fracPos * fracNeg * 3    # p * p * (1-p)
    p_t3 = fracPos * fracPos * fracPos        # p * p * p
    
    probs = [p_t0, p_t1, p_t2, p_t3]    
    ############################################################################

    print 'Fraction of Positive Edges: %0.4f' % (fracPos)
    print 'Fraction of Negative Edges: %0.4f' % (fracNeg)

    for i in range(4):
        print "Probability of Triad t%d: %0.4f" % (i, probs[i])

# Problem 2.4 Functions
def createCompleteNetwork(networkSize):
    """
    :param - networkSize: Desired number of nodes in network

    return type: Graph
    return: Returns complete network on networkSize
    """
    completeNetwork = None
    ############################################################################
    # TODO: Your code here!
    #Add a edge between every node to every other node
    completeNetwork = snap.TUNGraph.New()
    for i in range (1, networkSize + 1):
        completeNetwork.AddNode(i)
    for i in range (1, networkSize + 1):
        for j in range (i + 1, networkSize + 1):
            if i!=j and completeNetwork.IsEdge(i, j) == False:
                completeNetwork.AddEdge(i, j)               
                
    ############################################################################
    return completeNetwork

def assignRandomSigns(G):
    """
    :param - G: Graph

    return type: dictionary (key = node pair (a,b), value = sign)
    return: For each edge, a sign (+, -) is chosen at random (p = 1/2).
    """
    signs = {}
    ############################################################################
    # TODO: Your code here!
    for i in range (1, G.GetNodes() + 1):
        for j in range (i + 1, G.GetNodes() + 1):
            ran = random.random()  
            if ran >= 0.5:
                signs [(i,j)] = 1
            else:
                signs[(i,j)] = -1 
            
    ############################################################################
    return signs

def runDynamicProcess(G, signs, num_iterations):
    """
    :param - G: Graph
    :param - signs: Dictionary of signs (key = node pair (a,b), value = sign)
    :param - num_iterations: number of iterations to run dynamic process

    Runs the dynamic process described in problem 2.3 for num_iterations iterations.
    """
    ############################################################################
    # TODO: Your code here!
    #num_iterations = 10000
    for i in range (0, num_iterations):
        rTriad = random.sample(range (1, G.GetNodes() + 1),  3)
        rTriad = sorted(rTriad)
        pcount, ncount = 0, 0
        isBal = False 
        # for every triad count the positive and negavtive edged. The count will reveal if its
        # balanced or not
        if signs[(rTriad[0], rTriad[1])] == 1:
            pcount += 1
        else:
            ncount += 1 
    
        if signs[(rTriad[1], rTriad[2])] == 1:
            pcount += 1
        else:
            ncount += 1 
        
        if signs[(rTriad[0], rTriad[2])] == 1:
            pcount += 1
        else:
            ncount += 1 

        if (pcount == 3 or pcount == 1):
            isBal = True
        
        # if its not balanced flip one edge at random
        if (isBal == False):
            rEdge = random.sample(rTriad, 2)
            rEdge = sorted(rEdge)
            signs[(rEdge[0], rEdge[1])] = (-1) * signs[(rEdge[0], rEdge[1])]

        
    ############################################################################

def isBalancedNetwork(G, signs):
    """
    :param - G: Graph
    :param - signs: Dictionary of signs (key = node pair (a,b), value = sign)

    return type: Boolean
    return: Returns whether G is balanced (True) or not (False).
    """
    isBalanced = False
    ############################################################################
    # TODO: Your code here!
    Faction1 = []
    Faction2 = []
    isBalanced = True
    # if every edge is +ve the its balanced graph
    for i in range (1, G.GetNodes() + 1):
        for j in range (i + 1, G.GetNodes() + 1):
            if(signs[(i, j)] == (-1)):
                isBalanced = False
                
    if isBalanced == True:
        return isBalanced
    
    #divide nodes of graph into two factions
    #if all the nodes in factions are connected with +ve edges and
    #if edges between two factions are -ve then the graph is balanced
    isBalanced = True
    for NI in G.Nodes():
        if Faction1.count(NI.GetId()) == 0 and Faction2.count(NI.GetId()) == 0 :
            Faction1.append(NI.GetId())
        for i in range (0, NI.GetDeg() ):
            nid = NI.GetNbrNId (i)
            if NI.GetId() < nid:
                n1 = NI.GetId()
                n2 = nid
            else:
                n1 = nid
                n2 = NI.GetId()
                
            if signs[(n1,n2)] == -1:
                if Faction1.count(NI.GetId()) == 1:
                    if Faction1.count(nid) == 1:
                        isBalanced = False
                        break
                    else :
                        if Faction2.count(nid) == 0:
                            Faction2.append(nid)
                elif Faction2.count(NI.GetId()) == 1:
                    if Faction2.count(nid) == 1:
                        isBalanced = False
                        break
                    else :
                        if Faction1.count(nid) == 0:
                            Faction1.append(nid)                        
                       
            else:
                if Faction1.count(NI.GetId()) == 1:
                    if Faction2.count(nid) == 1:
                        isBalanced = False
                        break
                    else:
                        if Faction1.count(nid) == 0:
                            Faction1.append(nid)
                elif Faction2.count(NI.GetId()) == 1:
                    if Faction1.count(nid) == 1:
                        isBalanced = False
                        break
                    else :
                        if Faction2.count(nid) == 0:                        
                            Faction2.append(nid)
            
        
          
    #print isBalanced
    ############################################################################
    return isBalanced

def computeNumBalancedNetworks(numSimulations):
    """
    :param - numSimulations: number of simulations to run

    return type: Integer
    return: Returns number of networks that end up balanced.
    """
    numBalancedNetworks = 0

    for iteration in range(0, numSimulations):
        # (I) Create complete network on 10 nodes
        simulationNetwork = createCompleteNetwork(10)

        # (II) For each edge, choose a sign (+,-) at random (p = 1/2)
        signs = assignRandomSigns(simulationNetwork)

        # (III) Run dynamic process
        num_iterations = 1000000
        runDynamicProcess(simulationNetwork, signs, num_iterations)

        # determine whether network is balanced
        if isBalancedNetwork(simulationNetwork, signs):
            numBalancedNetworks += 1

    return numBalancedNetworks

def main():
    filename = "epinions-signed.txt"

    # load Graph and Signs
    epinionsNetwork = snap.LoadEdgeList(snap.PUNGraph, filename, 0, 1)
    signs = loadSigns(filename)

    # Compute Triad Counts
    triad_count = computeTriadCounts(epinionsNetwork, signs)

    # Problem 2.1a
    print "Problem 2.1a"
    for i in range(4):
        print "Count of Triad t%d: %d" % (i, triad_count[i])

    total_triads = float(sum(triad_count)) if sum(triad_count) != 0 else 1
    for i in range(4):
        print "Fraction of Triad t%d: %0.4f" % (i, triad_count[i]/total_triads)

    # Problem 2.1b
    print "Problem 2.1b"
    displayStats(epinionsNetwork, signs)

    # Problem 2.4
    print "Problem 2.4"
    networkSize = 10
    numSimulations = 100
    numBalancedNetworks = computeNumBalancedNetworks(numSimulations)
    print "Fraction of Balanced Networks: %0.4f" % (float(numBalancedNetworks)/float(numSimulations))


if __name__ == '__main__':
    main()
