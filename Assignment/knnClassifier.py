from random import random,randint
import math

def makeTrainingSet(filename):

    #split the file into separate lines for each record
    #and into separate elements for each variable
    data=[line.split(',') for line in file(filename)]

    #cast numerical data into float values
    #and remove spaces and endlines from
    #the final element (>50K and <=50K)
    for i in range(0,len(data)):
        data[i][1] = float(data[i][1])/100
        data[i][11] = float(data[i][11])/100
        data[i][12] = float(data[i][12])/100
        data[i][13] = float(data[i][13])/100
        data[i][15] = data[i][15].replace('\n', '')
        data[i][15] = data[i][15].replace(' ', '')
     
    return data
	
	
def getdistances(data, query):
    #make a list to put the distances into
    distancelist=[]
    num_dist = 0
    cat_dist = 0
    
    # Loop over every item in the training set
    for i in range(len(data)):
        cat_dist = 0
        num_dist = 0
        
        #compute the numerical distance between each
        #numerical variable of the training set and the query
        #using euclidian distance
        num_dist=math.sqrt((data[i][1]-(query[1]/100))**2)
        num_dist= num_dist + math.sqrt((data[i][11]-query[11])**2)
        num_dist= num_dist + math.sqrt((data[i][12]-query[12])**2)
        num_dist= num_dist + math.sqrt((data[i][13]-query[13])**2)
        
        #compute the categorical distance between each
        #numerical variable of the training set and the query
        #add one to the distance if the variables are identical
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
            
        # Add the distance and the index to the distance list
        distancelist.append([num_dist+cat_dist,data[i][15]])
      
    # Sort the distance list by distance
    distancelist.sort()
    return distancelist
	
	
def knnestimate(data,query,k=20):

    # Get the sorted distances between the query and
    # each record in the training set
    dlist = getdistances(data, query)
    o50k_count = 0
    u50k_count = 0

    # for the top k results (the most similar records)
    # count the number of target variables of each type
    for i in range(k):
        if dlist[i][1] == '<=50K':
            u50k_count = u50k_count + 1
        else:
            o50k_count = o50k_count + 1

    # return the category with the highest number of
    # records in it
    if u50k_count > o50k_count:
      return '<=50K'
    else:
      return '>50K'


def main():

    #make the trainingset and the test set by reading
    # in from files
    trainingSet = makeTrainingSet("data/trainingSet.txt")
    testSet = makeTrainingSet("data/queries.txt")

    # make a list to store the classifiers results in
    results = []

    # loop through the queries
    for i in range(len(testSet)):
        # classify each record using the training set
        ans = knnestimate(trainingSet, testSet[i])
        # put the id of the test set and the classification
        # into the results list
        testSet[i][15] = ans
        results.append(testSet[i][0]+"," + testSet[i][15])
        
    # print the results list to a file
    out_file = open("solutions/OutputData.txt", "wt")
    for i in range(0, len(results)):
        out_file.write(str(results[i]))
        out_file.write("\n")
       
    out_file.close()

    print "Program finished."

main()
