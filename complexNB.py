import math

def getInputData(datafile):
  data=[line.split(',') for line in file(datafile)]
  for i in range(0,len(data)):
      # convert the numeric data type from
      # strings to floats and ints.
      data[i][1] = int(data[i][1])
      data[i][3] = int(data[i][3])
      data[i][5] = int(data[i][5])
      data[i][11] = int(data[i][11])
      data[i][12] = int(data[i][12])
      data[i][13] = int(data[i][13])
      # strip the \n characters from the
      # right side of the target variable
      data[i][15] = data[i][15].replace('\n', '')
      data[i][15] = data[i][15].replace('\r', '')
      data[i][15] = data[i][15].replace(' ', '')
  return data

class nbayes:
      o50k_data = []
      u50k_data = []
      o50k_cat_probs = {}
      u50k_cat_probs = {}
      o50k_num_prob_dist = 0
      u50k_num_prob_dist = 0
      
      def __init__(self, data):
            for row in data:
                  target = row[15]
                  target.replace('\n', '')
                  target.replace('\r', '')
                  target.replace(' ', '')
                  
                  if target == '>50K':
                        self.o50k_data.append(row)
                  else:
                      self.u50k_data.append(row)

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
      #This prob dist specifies the prob of the
      #numeric feat taking a particular value
      #to create a prob dist we need to compute
      #the mean and variance of the feat values
      #and pass these to the make_gaussian func
      def getNumProbDist(self, data):
            #compute the mean
            total = 0
			
            for row in data:
                  total1 = total + row[1]
                  total2 = total + row[3]
                  total3 = total + row[5]
                  total4 = total + row[11]
                  total5 = total + row[12]
                  total6 = total + row[13]
            mean1 = float(total1)/len(data)
            mean2 = float(total1)/len(data)
            mean3 = float(total1)/len(data)
            mean4 = float(total1)/len(data)
            mean5 = float(total1)/len(data)
            mean6 = float(total1)/len(data)
			
            for row in data:
                  total1 = total1 + (row[1]-mean1)**2
                  total2 = total2 + (row[3]-mean2)**2
                  total3 = total3 + (row[5]-mean3)**2
                  total4 = total4 + (row[11]-mean4)**2
                  total5 = total5 + (row[12]-mean5)**2
                  total6 = total6 + (row[13]-mean6)**2
				  
            variance1 = float(total1)/len(data)
            variance2 = float(total2)/len(data)
            variance3 = float(total3)/len(data)
            variance4 = float(total4)/len(data)
            variance5 = float(total5)/len(data)
            variance6 = float(total6)/len(data)
			
            result = self.make_gaussian(mean1, variance1)
            return result

      def make_gaussian(self, mu, sigma):
            return (lambda x: ( (1.0/math.sqrt(2*math.pi*sigma)) * math.e**( (-1.0*((x-mu)**2))/(2*sigma) ) ) )

      def train(self):
            self.o50k_cat_probs = self.getCatProbs(self.o50k_data)
            print self.getNumProbDist(self.o50k_data)
            self.o50k_num_prob_dist = self.getNumProbDist(self.o50k_data)
            self.u50k_cat_probs = self.getCatProbs(self.u50k_data)
            self.u50k_num_prob_dist = self.getNumProbDist(self.u50k_data)
 

      def classify(self, query):
            #compute the probability of
            #the explanatory variable taking
            #the values they do given that
            #the target variable = C1
            c1np = self.o50k_num_prob_dist
            c1cp = self.o50k_cat_probs.get(query[1])
            c1_prob = c1cp * c1np 
            #compute the probability of
            #the explanatory variable taking
            #the values they do given that
            #the target variable = C1
            c2np = self.u50k_num_prob_dist
            c2cp = self.u50k_cat_probs.get(query[1])
            c2_prob = c2cp * c2np
            if c1_prob > c2_prob:
                  return '>50k'
            elif c1_prob < c2_prob:
                  return '<=50k'
            else:
                  return 'unknown'

def main():
      data = getInputData('trainingSet.txt')
      test = getInputData('testSet.txt')


      p = nbayes(data)
      p.train()
      
      pans = []
      for row in test:
            pans.append(p.classify(row))
      print ("n-bayes")
      print pans

	  #count how many of the test set each
	  #classifier got right.
      pcorrect = 0
      for i in range(0, len(kans)):
            if i < 10:
                  if pans[i] == 'C1':
                        pcorrect = pcorrect + 1
            else:
                  if pans[i] == 'C2':
                        pcorrect = pcorrect + 1
      print("n-bayes correct: " + str(pcorrect))
      print ("finsihed processing!")

main()
