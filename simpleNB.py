import re #regular expression library
import math


def getwords(doc):
  splitter=re.compile('\\W*') 
  #print doc
  words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  
  # Return the unique set of words only
  return dict([(w,1) for w in words])


class classifier:
  def __init__(self,getfeatures,filename=None):
    # Counts of feature/category combinations
    self.fc={}
    # Counts of documents in each category
    self.cc={}
    self.getfeatures=getfeatures

    
  # Increase the count of a feature/category pair
  def incf(self,f,cat):
    self.fc.setdefault(f,{}) 
    self.fc[f].setdefault(cat,0)
    self.fc[f][cat]+=1

  # Increase the count of a category
  def incc(self,cat):
    self.cc.setdefault(cat,0)
    self.cc[cat]+=1

  # The number of times a feature has appeared in a category
  def fcount(self,f,cat):
    if f in self.fc and cat in self.fc[f]:
      return float(self.fc[f][cat])
    return 0.0

  # The number of items in a category
  def catcount(self,cat):
    if cat in self.cc:
      return float(self.cc[cat])
    return 0

  # The total number of items
  def totalcount(self):
    return sum(self.cc.values( ))

  # The list of all categories
  def categories(self):
    return self.cc.keys( )


  def trainrecord(self,item,cat):
    features=self.getfeatures(item)
    #print features
    #print '\n'
    # Increment the count for every feature with this category
    for f in features:
      self.incf(f,cat)
    # Increment the count for this category
    self.incc(cat)



  def fprob(self,f,cat):
    if self.catcount(cat)==0: return 0

    # The total number of times this feature appeared in this 
    # category divided by the total number of items in this category
    return self.fcount(f,cat)/self.catcount(cat)


  def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
    # Calculate current probability
    basicprob=prf(f,cat)

    # Count the number of times this feature has appeared in
    # all categories
    totals=sum([self.fcount(f,c) for c in self.categories()])

    # Calculate the weighted average
    bp=((weight*ap)+(totals*basicprob))/(weight+totals)
    return bp



class naivebayes(classifier):
  
  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    #used the hold the thresholds for each category
    #(this is explained later in the lab)
    self.thresholds={}
  
  def docprob(self,item,cat):
    features=self.getfeatures(item)   

    # Multiply the probabilities of all the features together
    p=1
    for f in features: p*=self.weightedprob(f,cat,self.fprob)
    return p


  def prob(self,item,cat):
    catprob=self.catcount(cat)/self.totalcount()
    docprob=self.docprob(item,cat)
    return docprob*catprob

  
  def setthreshold(self,cat,t):
    self.thresholds[cat]=t
    
  def getthreshold(self,cat):
    if cat not in self.thresholds: return 1.0
    return self.thresholds[cat]

 
  def classify(self,item,default=None):
    probs={}
    # Find the category with the highest probability
    max=0.0
    for cat in self.categories():
      probs[cat]=self.prob(item,cat)
      if probs[cat]>max: 
        max=probs[cat]
        best=cat

    # Make sure the probability exceeds threshold*next best
    for cat in probs:
      if cat==best: continue
      if probs[cat]*self.getthreshold(best)>probs[best]: return default
    return best

def sampletrain(cl):
  cl.trainrecord('Nobody owns the water.','good')
  cl.trainrecord('the quick rabbit jumps fences','good')
  cl.trainrecord('buy pharmaceuticals now','bad')
  cl.trainrecord('make quick money at the online casino','bad')
  cl.trainrecord('the quick brown fox jumps','good')


# dump some sample training data in a classifier
def train(cl, filename):

    file = open(filename)
    right = 0

    for line in file:
        line.strip()
        line_list = line.split(',')
        #age = float(line_list[1])
        workclass = line_list[2]
        #fnlwgt = float(line_list[3])
        education = line_list[4]
        #educationNum = float(line_list[5])
        maritalStatus = line_list[6]
        occupation = line_list[7]
        relationship = line_list[8]
        race = line_list[9]
        sex = line_list[10]
        #capitalGain = float(line_list[11])
        #capitalLoss = float(line_list[12])
        #hoursPerWeek = float(line_list[13])
        nativeCountry = line_list[14]
        target = line_list[15]
        target = target.replace('\n', '')
        target = target.replace('\r', '')
        target = target.replace(' ', '')

        record = ' '.join([workclass, education, maritalStatus, occupation, relationship, race, sex, nativeCountry])
        cl.trainrecord(record, target)
        
        if cl.classify(record) == target:
            right+=1

    print '--------'
    print right
    print 'right out of'
    print cl.totalcount()
    print '--------'

    file.close()

def classifyall(cl, filename):

    file = open(filename)

    over50k = 0
    under50k = 0
    
    for line in file:
        line.strip()
        line_list = line.split(',')
        #age = float(line_list[1])
        workclass = line_list[2]
        #fnlwgt = float(line_list[3])
        education = line_list[4]
        #educationNum = float(line_list[5])
        maritalStatus = line_list[6]
        occupation = line_list[7]
        relationship = line_list[8]
        race = line_list[9]
        sex = line_list[10]
        #capitalGain = float(line_list[11])
        #capitalLoss = float(line_list[12])
        #hoursPerWeek = float(line_list[13])
        nativeCountry = line_list[14]

        record = ' '.join([workclass, education, maritalStatus, occupation, relationship, race, sex, nativeCountry])

        if cl.classify(record) == '<=50K':
            under50k+=1
        else:
            over50k+=1

    print 'classifying:'
    print '>50K: '
    print over50k
    print '<=50K: '
    print under50k
    print '-----'
        
    file.close()

def main():
    cl = naivebayes(getwords)
    #sampletrain(cl)
    #print cl.prob('casino quick', 'bad')
    train(cl, 'trainingSet.txt')
    #print cl.classify('Private Assoc-voc Never-married Prof-specialty Not-in-family White Female United-States')
    classifyall(cl, 'trainingSet.txt')

    print 'cat count'
    print ' -----'
    print '>50k:'
    print cl.catcount('>50K')
    print '<=50K:'
    print cl.catcount('<=50K')

main()
