from csv import DictReader,DictWriter
class marcoveChain:
    def __init__(self,path,delimeter = " "):
# read the file sequence and automaticly create tranistion probability table
#         
        self.filePath = path
        self.delimeter = delimeter
        self.dataList = None
# this dict store initial type or probabilityMatrics it store count
# for a perticular state and join probability of a perticular state
# which means which state come after that state and how many times        
        self.trasitionStates = {}
# include uniques words or states in a dict use to initialize self.trasitionState's
# sub state    
        self.inititalStates = {}
# use transition states dictionary and make probabitily 
# it contain probability rather than counts         
        self.probabilityMatrix = {}
# use to lead sequence and generate it transitionstates dictionany and than finaly
# probability matrix        
    def loadDataSequenceFile(self):
        try:
            with open(self.filePath,'r') as ar:
                self.dataList = ar.read().split(self.delimeter)
            # print(self.dataList) 
        except Exception as e:
            print(e)
            return False 
        self.makeTrasitionStatesWithProbability()
        self.generateProbabilityMatrix()                  
        return True 
# write final transition matrix to the file         
    def writeTrasitionMatrix(self):
        try:
            with open('tranistionMatrix.csv','w') as wr:
                w = DictWriter(wr,fieldnames=list(self.probabilityMatrix))
                w.writeheader()
                for i,j in self.probabilityMatrix.items():
                    w.writerow(j)    
        except Exception as e:
            print(e)    
# read file and directily generate probability matrix             
    def readTransitionMatrix(self):
        lis = []
        try:
            with open('tranistionMatrix.csv','r') as re:
                r = DictReader(re)
                print(' read ')
                for i in r:
                    lis.append(i)
                #lis.append({})    
                self.transformCsvToProbabilityMatrix(lis)       
        except Exception as e:
            print(e)    
 # use dictonary list and turn it into prbability matrix           
    def transformCsvToProbabilityMatrix(self,lis):
        if len(lis) == len(lis[0]):
            self.probabilityMatrix = {}
            l = list(lis[0])
            for i in range(len(l)):
                self.probabilityMatrix[l[i]] = lis[i]
            print(self.probabilityMatrix)    
        else:
            raise Exception('matrix is not square')
# use when sequence is loaded store the count or a perticular state and 
# its join states a state that come after in dictionary        
    def makeTrasitionStatesWithProbability(self):
        self.initializeStates()
        for i in range(len(self.dataList)-1):
            state = self.dataList[i]
            if self.trasitionStates.__contains__(state):
                self.trasitionStates[state]['count'] += 1
                self.trasitionStates[state]['connections'][self.dataList[i+1]] += 1
            else:
                self.trasitionStates[state] = {'count':1,'connections':self.inititalStates.copy()}  
# use to initialize trasitionStates connections or join states
    def initializeStates(self):
        for i in self.dataList:
            if not self.inititalStates.__contains__(i):
                self.inititalStates[i] = 0  
# generate probability matrix from trasitionStates                  
    def generateProbabilityMatrix(self):
        currentCount = 0
        for i,j in self.trasitionStates.items():
            self.probabilityMatrix[i] = {}
            currentCount = j['count']
            for s,p in j['connections'].items():
                self.probabilityMatrix[i][s] = p/currentCount
# try to generate best sequence with high probability with first letter and limit
#
    def generateBestSequence(self,firstLetter,limit = 2):
        S = 0
        P = 1
        prob = 0
        connectionName = firstLetter
        sequence = []
        if self.probabilityMatrix.__contains__(firstLetter):
            for i in range(limit):
                for k,j in self.probabilityMatrix[connectionName].items():
                    if j > prob:
                        prob = j
                        P *= prob
                        print(P,j,k)                        
                        connectionName = k
                prob = 0        
                sequence.append(connectionName)
            print(P)    
            return [sequence,P]    
# tell the probability of a sequence entered
    def generateProbability(self,lis):
        probability = 1
        for i in range(len(lis)-1):
            for k,j in self.probabilityMatrix[lis[i]].items():
                if k == lis[i+1]:
                    probability *= j        
        return probability    


c = marcoveChain('sequence.txt')
c.loadDataSequenceFile()
print(" generate best sequence ")
print(c.generateBestSequence('sunny'))
print(" generate probability of a sequence ")
print(c.generateProbability(['sunny', 'cloudy', 'sunny','sunny']))
c.writeTrasitionMatrix()
c.readTransitionMatrix()