# in this algorithm we shall consider all common attributes of a perticular label 
# and predict on the bases of common attributes
# of a label
from csv import DictReader
class find_S:
    def __init__(self):
# fearures are x axis or attributes which we are going to take common attributes 
# they are in the form of list of attributes [[attr1,attr2,...],....]       
        self.features = []
# label is yes, or no after these or the result of attributes which
# could be any thing
# for each list of attributes there is only one label which is one word
# [label1,label2,.....]
        self.labels = []
# hypothisis will take all the common attributes of a perticular label
# it will replace self.general in place of a conflicted attributes        
        self.hypothisis = {}
# columns of a dataset 
# row of a dataset        
        self.columns = int
        self.rows = int
        self.general = '?'
    def fit(self,x,y):
        self.features = x
        self.labels = y
        self.columns = len(x[0])
        self.rows = len(x)
        self.makeHypothesis()

    def makeHypothesis(self):
        for i in range(self.rows):
# compare attributes of a tuple of dataset or single dataset
# with existing hypothesis of that perticular label            
            self.compare(self.features[i],self.labels[i])
    def compare(self,data,label):
# if we do not have any hypothesis of that perticular label than we consider
# this first tuple of that perticular label our hypothisis         
        if not dict.__contains__(self.hypothisis,label):
            self.hypothisis[label] = data
        else:
# if we have hypothisis of a perticular label than we shale compare it 
# the data tuple in case of any conflict we shall put self.general on its place
# in our hypothisis self.general means we donot know any thing about it            
            for i in range(self.columns):
                if data[i] != self.hypothisis[label][i]:
                    if data[i] != self.general:
                       self.hypothisis[label][i] = self.general
# this will return hypothesis in the form of list
# [[label,[hypothisi attribues]],..]                       
    def reHypothisis(self):
        lis = []
        for i,j in self.hypothisis.items():
            lis.append([i,j])
        return lis    

    def predict(self,data):
        l = self.reHypothisis()
        ans = {}
        for i in l:
            ans[i[0]] = self.check(data,i[1])
        return ans
    def check(self,data,l):
        for i in range(self.columns):
            if l[i] != data[i]:
                if l[i] != self.general:
                    return False  
        return True            


                          

f = find_S()
da = ''
x = []
y = []
with open('find_sdata.csv','r') as re:
    da = DictReader(re)
    for i in da:
        lis = []
        for j,k in i.items():
            if j == 'enjoy':
                 y.append(k)
            else:
                lis.append(k)     
        x.append(lis)        

f.fit(x,y)
print(f.hypothisis)
print(f.predict(['sunny', 'warm', 'hs', 'strong', 'sd', 'same']))

        
