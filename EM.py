# randome probability  ,p1,p2...
# chose main attribute like H from H,T where H,T are the name of columns
#foreachTuple total=sum(sum of all attributes A) where A={H,T} A have both H,T value of attributs
# foreach Attribute of a tuple A={H,T} where A can contain Value of H and T
#foreach Probability p={p1,p2} 
# r{n} p^A*(1-p)^(total-A)
# in this case p can be p1,p2 and A can be T,H 
#  where p is a probability A attributes and total is sum of all attributes in a tuble
#  r{n} is storage location for storing return and n is the number of probability
# E{n} = r{n}/r{1}+r{2}..r{n} E{n} is a expected probability of a result r{n}  
# in this case E{1} = r{1}/r{1}+r{2} , E{2} = r{2}/r{1}+r{2}  
# E{N}*A, multipuly expected probability with Attribute Value
#  
from csv import DictReader
from math import factorial as fact
class expectationMaximum:
    def __init__(self,probabilityDict,expectationAttribute,filePath):
        self.probabilityDict = probabilityDict
        self.expectationAttribute = expectationAttribute
        self.probabilityData = {}
        self.filePath = filePath 
        self.dataList = []
        self.initializeProbabilityDataList()
        self.loadData()
    def initializeProbabilityDataList(self):
        for i in self.probabilityDict:
            self.probabilityData[i] = []
    def clearProbData(self):
        print(" +++++++++++++++++++++++++++++++new iteration started++++++++++++++++++++++++++ ")
        for i in self.probabilityData:
            self.probabilityData[i].clear()    

    def loadData(self):
        try:
            with open(self.filePath,'r') as ar:
                rea = DictReader(ar)
                for i in rea:
                    self.dataList.append(i)
        except Exception as e:
            self.dataList.clear()
            return False            
        if not self.dataList[0].__contains__(self.expectationAttribute):
            self.dataList.clear()
            return False
        return True 

    def strDict(self,i):
        di = ""
        for k,j in i.items():
            di += k
            di+= " : "
            di+=str(j)
            di+=" , "
        return di    
    def printProbabilityData(self):
        for i,j in self.probabilityData.items():
            print(" probability table of : "+i)
            for k in j:
                print(self.strDict(k))
    def printProbabilityDict(self):
        print(" current Probability ",self.strDict(self.probabilityDict))    
    def printData(self):
        for i in self.dataList:
            print(self.strDict(i))               

    def combination(self,n,r):
        return (fact(n)/(fact(n-r)*fact(r)))

    def binomialFormula(self,probability,attributeValue,TotalTupleValue):
        #c = self.combination(TotalTupleValue,attributeValue)
        #print(" combination  ",c," attributeValue ",attributeValue," totalValue ",TotalTupleValue)
        return (pow(probability,attributeValue)*pow((1-probability),(TotalTupleValue-attributeValue)))    
    def getTupleTotal(self,t):
        total = 0
        Tuple ={}
        value = 0
        for i,j in t.items():
            value = int(j)
            Tuple[i] = value
            total += value
        return [total,Tuple]  
    def sendCopyKeys(self,ti):
        to = {}
        for i in ti: 
            to[i] = 0
        return to       
    def initializeProbabilityData(self,t):
        currentProbabilityData = {}
        cop = None
        print(" initializing tuple ",t)
        for i in self.probabilityDict:
            self.probabilityData[i].append(self.sendCopyKeys(t))
            currentProbabilityData[i] = len(self.probabilityData[i])-1
        return currentProbabilityData    
    def clearProbabilityDataList(self):
        pass    
    def insertProbabilityData(self,binomia,dataName,data,probabilityDataDic):
        binomialTotal = 0.0
        v = 0
        for i,j in binomia.items():
            binomialTotal += j
        for k,l in probabilityDataDic.items():
            v = ((binomia[k]/binomialTotal)*data) 
            self.probabilityData[k][l][dataName] = v
            print(" p ",k,"b ",binomia[k],"tB ",binomialTotal,"d ",data,"v ",v)   

    def SumProbability(self):
        totalProbability = {}
        for i,j in self.probabilityData.items():
            total = {}
            for m in j:
                for k,l in m.items():
                    if total.__contains__(k):
                        total[k] += l
                    else:
                        total[k] = l 
            totalProbability[i] = total  
        return totalProbability
    def getMainPropability(self,totalProb):
        print(" total probability ")
        print(self.strDict(totalProb))
        newProbability = {}
        total = 0
        for i,j in totalProb.items():
            total = 0 
            for l,k in j.items():
                total += k
            newProbability[i] = j[self.expectationAttribute]/total
        return newProbability        
    
    def compareProbabilityAndChange(self,newProbability):
        for i,j in newProbability.items():
            if self.probabilityDict[i] != j:
                return True
        return False        
    def getNewProbability(self):
        binomial = {}
        for i in self.dataList:
            l = self.getTupleTotal(i)
            data = self.initializeProbabilityData(l[1])
            print(l[1])
            for o,m in l[1].items():
                for k,f in self.probabilityDict.items():
                 #   print("+++++++++++++++++++++++++")
                 #   print(" probabilityName  ",k," attribute Name ",o)
                    binomial[k] = self.binomialFormula(f,m,l[0])
                    # print(" prob ",k," value ",f," att",o," value ",m," binomial ",binomialValue)
                  #  print(" binomial ans  ",binomial[k])
                  #  print("+++++++++++++++++++++++++")
                print(" final binomial ",binomial)  
                self.insertProbabilityData(binomial,o,m,data)    
        newP = self.getMainPropability(self.SumProbability())
        self.printProbabilityData()
        return  [self.compareProbabilityAndChange(newP),newP]        
    
    def train(self):
        flag = True
        self.printData()
        print(" initialProbability ")
        self.printProbabilityDict()
        while True:
            l = self.getNewProbability()
            flag = l[0]
            if flag:
                self.probabilityDict = l[1]
                print(" current probability ")
                self.printProbabilityDict()
                self.clearProbData()
                
            else:
                break    







e = expectationMaximum({"coinA":0.60,"coinB":0.50},"H","headTail.csv")
e.train()
print(e.probabilityData)
