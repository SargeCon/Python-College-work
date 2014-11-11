from random import random,randint
import math

def makeTrainingSet(filename):
    
    data=[line.split(',') for line in file(filename)]
    for i in range(0,len(data)):
        data[i][1] = float(data[i][1])/100
        data[i][11] = float(data[i][11])/100
        data[i][12] = float(data[i][12])/100
        data[i][13] = float(data[i][13])/100
        data[i][15] = data[i][15].replace('\n', '')
        data[i][15] = data[i][15].replace(' ', '')
     
    return data
	
	
def getdistances(data, query):
    distancelist=[]
    num_dist = 0
    cat_dist = 0
    
    # Loop over every item in the dataset
    for i in range(len(data)):
        cat_dist = 0
        num_dist = 0
        #compute the numeric dist
        num_dist=math.sqrt((data[i][1]-(query[1]/100))**2)
        num_dist= num_dist + math.sqrt((data[i][11]-query[11])**2)
        num_dist= num_dist + math.sqrt((data[i][12]-query[12])**2)
        num_dist= num_dist + math.sqrt((data[i][13]-query[13])**2)
        
        #compute the categorical dist
        if not(data[i][2] == query[2]):
            cat_dist = 1
        if not(data[i][4] == query[4]):
            cat_dist += 1
        if not(data[i][6] == query[6]):
            cat_dist += 1
        if not(data[i][7] == query[7]):
            cat_dist += 1
        if not(data[i][8] == query[8]):
            cat_dist += 1
        if not(data[i][9] == query[9]):
            cat_dist += 1
        if not(data[i][10] == query[10]):
            cat_dist += 1
        if not(data[i][14] == query[14]):
            cat_dist += 1
        # Add the distance and the index
        distancelist.append([num_dist+cat_dist,data[i][15]])
      
    # Sort by distance
    distancelist.sort()
    return distancelist
	
	
def knnestimate(data,query,k=20):
    print 'working'
    # Get sorted distances
    dlist = getdistances(data, query)
    c1_count = 0
    c2_count = 0

    for i in range(k):
        if dlist[i][1] == '<=50K':
            c1_count = c1_count + 1
        else:
            c2_count = c2_count + 1
            
    if c1_count > c2_count:
      return '<=50K'
    else:
      return '>50K'


def main():
    trainingSet = makeTrainingSet("data/trainingSet.txt")
    testSet = makeTrainingSet("data/queries.txt")
    
    results = []

    for i in range(len(testSet)):
        ans = knnestimate(trainingSet, testSet[i])
        testSet[i][15] = ans
        results.append(testSet[i][0]+"," + testSet[i][15])
        
    
    out_file = open("solutions/C08373451.txt", "wt")
    for i in range(0, len(results)):
        out_file.write(str(results[i]))
        out_file.write("\n")
       
    out_file.close()
        

    print "Program finished."

main()
