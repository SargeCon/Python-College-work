from random import random,randint
import math

def makeTrainingSet(filename):
    trainingSet = []

    fin = open(filename,'r')

    # Read in file
    for line in fin:
        line = line.strip()
        line_list = line.split(',')

        # Create a dictionary for the line
        # ( assigns each attribute of the record (each item in the linelist)
        #   to an element of the dictionary, using the constant keys )
        record = {}
        id = float(line_list[0])
        age = float(line_list[1])
        workclass = line_list[4]
        fnlwgt = float(line_list[5])
        education = line_list[6]
        education-num = float(line_list[7])
        marital-status = line_list[8]
        occupation = line_list[9]
        relationship = float(line_list[10])
        race = line_list[11]
        sex = line_list[12]
        capital-gain = float(line_list[13])
        capital-loss = float(line_list[14])
        hours-per-week = float(line_list[15])
        native-country = line_list[16]
        target = line_list[17]

        # Add the dictionary to a list
        trainingSet.append({'input':(id, age, workclass, fnlwgt, education, education-num, marital-status, 
		occupation, relationship, race, sex, capital-gain, capital-lostt, hours-per-week, native-country),
		'result':target})       

    fin.close()
    return trainingSet
	
def makeTestSet(filename):
    testset = makeTrainingSet(filename)

    for record in testset:
        target = 'unknown'

    return testset


def euclidean(v1,v2):
  d=0.0
  for i in range(len(v1)):
    d+=(v1[i]-v2[i])**2
  return math.sqrt(d)


def getdistances(data,vec1):
  distancelist=[]
  
  # Loop over every item in the dataset
  for i in range(len(data)):
    vec2=data[i]['input']
    
    # Add the distance and the index
    distancelist.append((euclidean(vec1,vec2),i))
  
  # Sort by distance
  distancelist.sort()
  return distancelist

def knnestimate(data,vec1,k=5):
  # Get sorted distances
  dlist=getdistances(data,vec1)
  avg=0.0
  
  # Take the average of the top k results
  for i in range(k):
    idx=dlist[i][1]
    avg+=data[idx]['result']
  avg=avg/k
  return avg

def inverseweight(dist,num=1.0,const=0.1):
  return num/(dist+const)


def subtractweight(dist,const=1.0):
  if dist>const: 
    return 0
  else: 
    return const-dist

def gaussian(dist,sigma=5.0):
  return math.e**(-dist**2/(2*sigma**2))


def weightedknn(data,vec1,k=5,weightf=gaussian):
  # Get distances
  dlist=getdistances(data,vec1)
  avg=0.0
  totalweight=0.0
  
  # Get weighted average
  for i in range(k):
    dist=dlist[i][0]
    idx=dlist[i][1]
    weight=weightf(dist)
    avg+=weight*data[idx]['result']
    totalweight+=weight
  if totalweight==0: return 0
  avg=avg/totalweight
  return avg


def dividedata(data,test=0.05):
  trainset=[]
  testset=[]
  for row in data:
    if random()<test:
      testset.append(row)
    else:
      trainset.append(row)
  return trainset,testset
  

def testalgorithm(algf,trainset,testset):
  error=0.0
  for row in testset:
    guess=algf(trainset,row['input'])
    error+=(row['result']-guess)**2
    #print row['result'],guess
  #print error/len(testset)
  return error/len(testset)


def crossvalidate(algf,data,trials=100,test=0.1):
  error=0.0
  for i in range(trials):
    trainset,testset=dividedata(data,test)
    error+=testalgorithm(algf,trainset,testset)
  return error/trials


def rescale(data,scale):
  scaleddata=[]
  for row in data:
    scaled=[scale[i]*row['input'][i] for i in range(len(scale))]
    scaleddata.append({'input':scaled,'result':row['result']})
  return scaleddata


def probguess(data,vec1,low,high,k=5,weightf=gaussian):
  dlist=getdistances(data,vec1)
  nweight=0.0
  tweight=0.0
  
  for i in range(k):
    dist=dlist[i][0]
    idx=dlist[i][1]
    weight=weightf(dist)
    v=data[idx]['result']
    
    # Is this point in the range?
    if v>=low and v<=high:
      nweight+=weight
    tweight+=weight
  if tweight==0: return 0
  
  # The probability is the weights in the range
  # divided by all the weights
  return nweight/tweight
  

def main():
    trainingSet = []
    trainingFile = "annual-income-training.data"
    trainingSet = makeTrainingSet(trainingFile)

    testFile = "annual-income-test.data"
    testSet = makeTestSet(testFile)
	
	
	 for i in range(len(testSet)):
		knnestimate(trainingSet, testSet[i]['input'], k=5)

    # add call to appropriate function

    print "Program finished."
    
main()
