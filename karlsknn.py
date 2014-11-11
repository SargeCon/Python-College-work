import math

# Getting the data:

def getInputData(datafile):
  
  data=[line.split(',') for line in file(datafile)]
  
  for i in range(0,len(data)):
    
      # convert numeric data types from strings to ints.

      # age
      data[i][1] = int(data[i][1])
      
      # capital-gain
      data[i][11] = int(data[i][11])

      # capital-loss
      data[i][12] = int(data[i][12])

      # hours-per-week
      data[i][13] = int(data[i][13])
      
      
      # strip the \n characters from the
      # right side of the target variable
      data[i][15] = data[i][15].rstrip('\n')
      
  return data



# -------------------------------------------------

class knn:
      max_val = 100.0
      my_data = []
      
      def __init__(self, data):
        
            self.my_data = data
            
            #normalise the numeric features

            for i in range(0, len(self.my_data)):

                  # age
                  self.my_data[i][1] = self.my_data[i][1]/self.max_val
                  
                  # capital-gain
                  self.my_data[i][11] = self.my_data[i][11]/self.max_val

                  # capital-loss
                  self.my_data[i][12] = self.my_data[i][12]/self.max_val

                  # hours-per-week
                  self.my_data[i][13] = self.my_data[i][13]/self.max_val





      def getdistances(self, query):
        
            distancelist=[]
            total_num_dist = 0
            total_cat_dist = 0

            
            # Loop over every item in the dataset
            for i in range(len(self.my_data)):
              
                  #compute the numeric dist
                  age_dist = math.sqrt((self.my_data[i][1]-(query[1]/self.max_val))**2)
                  cap_gain_dist = math.sqrt((self.my_data[i][11]-(query[11]/self.max_val))**2)
                  cap_loss_dist = math.sqrt((self.my_data[i][12]-(query[12]/self.max_val))**2)
                  weekly_hours_dist = math.sqrt((self.my_data[i][13]-(query[13]/self.max_val))**2)
                  
                  print self.my_data[i][1]
                  print(query[1]/self.max_val)
                  print self.my_data[i][11]
                  print(query[11]/self.max_val)
                  print self.my_data[i][12]
                  print(query[12]/self.max_val)
                  print self.my_data[i][13]
                  print(query[13]/self.max_val)


                  #compute the categorical dist

                  #workclass
                  if not(self.my_data[i][2] == query[2]):
                        workclass_dist = 1
                  else:
                        workclass_dist = 0


                  #education
                  if not(self.my_data[i][4] == query[4]):
                        education_dist = 1
                  else:
                        education_dist = 0


                  #marital-status
                  if not(self.my_data[i][6] == query[6]):
                        marital_dist = 1
                  else:
                        marital_dist = 0


                  #occupation
                  if not(self.my_data[i][7] == query[7]):
                        occupation_dist = 1
                  else:
                        occupation_dist = 0


                  #relationship
                  if not(self.my_data[i][8] == query[8]):
                        relationship_dist = 1
                  else:
                        relationship_dist = 0


                  #race
                  if not(self.my_data[i][9] == query[9]):
                        race_dist = 1
                  else:
                        race_dist = 0


                  #sex
                  if not(self.my_data[i][10] == query[10]):
                        sex_dist = 1
                  else:
                        sex_dist = 0


                  #native_country
                  if not(self.my_data[i][14] == query[14]):
                        country_dist = 1
                  else:
                        country_dist = 0


                  # Add up total distances
                  total_num_dist = age_dist + cap_gain_dist + cap_loss_dist + weekly_hours_dist
                  total_cat_dist = workclass_dist + education_dist + marital_dist + occupation_dist + relationship_dist + race_dist + sex_dist + country_dist

                  
                  # Add the distance and the index
                  distancelist.append([total_num_dist + total_cat_dist, self.my_data[i][15]])
                  
            # Sort by distance
            distancelist.sort()
            return distancelist

      


      
      # The kNN function returns the most frequent class
      # in the top k results
      #
      def knnestimate(self,query,k=20):
            # Get sorted distances
            dlist = self.getdistances(query)
            c1_count = 0
            c2_count = 0
            
            for i in range(k):
                if dlist[i][1] == ' <=50K':
                    c1_count = c1_count + 1
                else:
                    c2_count = c2_count + 1
                        
            if c1_count > c2_count:
                  return ' <=50K'
            else:
                  return ' >50K'



      # Return a % value of two inputs
      def percentage(self, part, whole):
          return 100 * float(part)/float(whole)





def main():
    trainingSet = getInputData("trainingSet.txt")
    #crossvalidate(knnestimate, trainingSet)
    testSet = getInputData("testSet.txt")

    k = knn(trainingSet)

    correctValues = []

    for i in range(len(testSet)):
        result = testSet[i][15]
        correctValues.append(result)

    correct = 0
    incorrect = 0
    o = 0
    u = 0
    results = []

    for i in range(len(testSet)):
        ans = k.knnestimate(testSet[i])
        if ans == ' >50K':
            o += 1
        else:
            u += 1
        if ans == correctValues[i]:
            correct+=1
        else:
            incorrect+=1
        testSet[i][15] = ans
        results.append(testSet[i][0]+"," + testSet[i][15])
        
    print 'over'
    print o
    print 'under'
    print u
    print 'correct'
    print correct
    print 'incorrect'
    print incorrect

    
   # out_file = open("C08373451.txt", "wt")
   # for i in range(0, len(results)):
   #     out_file.write(str(results[i]))
   #     out_file.write("\n")
       
  #  out_file.close()
        

    # add call to appropriate function

    print "Program finished."

main()

