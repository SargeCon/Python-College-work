import math

def getInputData(datafile):
  data=[line.split(',') for line in file(datafile)]
  for i in range(0,len(data)):
      # convert the numeric data type from
      # strings to floats and ints.
      data[i][0] = int(data[i][0])
      # strip the \n characters from the
      # right side of the target variable
      data[i][2] = data[i][2].rstrip('\n')
  return data

class knn:
      max_val = 100.0 # used to normalise the data
      my_data = []
      
      def __init__(self, data):
            self.my_data = data
            #normalise the numeric feature
            for i in range(0, len(self.my_data)):
                  self.my_data[i][0] = self.my_data[i][0]/self.max_val

      def getdistances(self, query):
            distancelist=[]
            num_dist = 0
            cat_dist = 0
            # Loop over every item in the dataset
            for i in range(len(self.my_data)):
                  #compute the numeric dist
                  num_dist=math.sqrt((self.my_data[i][0]-(query[0]/self.max_val))**2)
                  #compute the categorical dist
                  if not(self.my_data[i][1] == query[1]):
                        cat_dist = 1
                  else:
                        cat_dist = 0
                  # Add the distance and the index
                  distancelist.append([num_dist+cat_dist,self.my_data[i][2]])
            # Sort by distance
            distancelist.sort()
            return distancelist

      #
      # The kNN function returns the most frequent class
      # in the top k results
      #
      def knnestimate(self,query,k=5):
            # Get sorted distances
            dlist=self.getdistances(query)
            c1_count = 0
            c2_count = 0
            for i in range(k):
                  if dlist[i][1] == 'C1':
                        c1_count = c1_count + 1
                  else:
                        c2_count = c2_count + 1
            if c1_count > c2_count:
                  return 'C1'
            else:
                  return 'C2'



class nbayes:
      c1_data = []
      c2_data = []
      c1_cat_probs = {}
      c2_cat_probs = {}
      c1_num_prob_dist = 0
      c2_num_prob_dist = 0
      
      def __init__(self, data):
            for row in data:
                  if row[2] == 'C1':
                        self.c1_data.append(row)
                  else:
                        self.c2_data.append(row)

	  # compute the relative frequencies of the
	  # 2nd explanatory variable taking on the
	  # values 'A', 'B' and 'C'
	  # and return a dictionary with these values
      def getCatProbs(self, data):
            a_count = 0
            b_count = 0
            c_count = 0
            probs = {}
            for row in data:
                  if row[1] == 'A':
                       a_count = a_count + 1
                  elif row[1] == 'B':
                        b_count = b_count + 1
                  else:
                        c_count = c_count + 1
            probs['A'] = float(a_count)/len(data)
            probs['B'] = float(b_count)/len(data)
            probs['C'] = float(c_count)/len(data)
            return probs

      #Create a normal probability distribution for
      #numeric features
      def getNumProbDist(self, data):
            #compute the mean
            total = 0
            for row in data:
                  total = total + row[0]
            mean = float(total)/len(data)
            #compute the variance
            #this measure how much a list of numbers
            #varies from the mean
            #it is calculated by averaging the squared
            #difference of every number from the mean
            for row in data:
                  total = total + (row[0]-mean)**2
            variance = float(total)/len(data)
            return self.make_gaussian(mean, variance)

      def make_gaussian(self, mu, sigma):
            return (lambda x: ( (1.0/math.sqrt(2*math.pi*sigma)) * math.e**( (-1.0*((x-mu)**2))/(2*sigma) ) ) )

      def train(self):
            self.c1_cat_probs = self.getCatProbs(self.c1_data)
            self.c1_num_prob_dist = self.getNumProbDist(self.c1_data)
            self.c2_cat_probs = self.getCatProbs(self.c2_data)
            self.c2_num_prob_dist = self.getNumProbDist(self.c2_data)
 

      def classify(self, query):
            #compute the probability of
            #the explanatory variable taking
            #the values they do given that
            #the target variable = C1
            c1np = self.c1_num_prob_dist(float(query[0])/100)
            c1cp = self.c1_cat_probs.get(query[1])
            c1_prob = c1cp * c1np 
            #compute the probability of
            #the explanatory variable taking
            #the values they do given that
            #the target variable = C1
            c2np = self.c2_num_prob_dist(float(query[0])/100)
            c2cp = self.c2_cat_probs.get(query[1])
            c2_prob = c2cp * c2np
            if c1_prob > c2_prob:
                  return 'C1'
            elif c1_prob < c2_prob:
                  return 'C2'
            else:
                  return 'unknown'

def main():
      data = getInputData('./ai2.txt')
      test = getInputData('./test_set.txt')

      k = knn(data)

      p = nbayes(data)
      p.train()
      
      kans = []
      pans = []
      for row in test:
            kans.append(k.knnestimate(row))
            pans.append(p.classify(row))
      print ("k-nn")
      print kans
      print ("n-bayes")
      print pans

	  #count how many of the test set each
	  #classifier got right.
	  #the 1st 10 are instances of C1 
	  #the 2nd 10 are instances of C2
      kcorrect = 0
      pcorrect = 0
      for i in range(0, len(kans)):
            if i < 10:
                  if kans[i] == 'C1':
                        kcorrect = kcorrect + 1

                  if pans[i] == 'C1':
                        pcorrect = pcorrect + 1
            else:
                  if kans[i] == 'C2':
                        kcorrect = kcorrect + 1

                  if pans[i] == 'C2':
                        pcorrect = pcorrect + 1
      print("knn correct: " + str(kcorrect))
      print("n-bayes correct: " + str(pcorrect))
      print ("finsihed processing!")

main()
