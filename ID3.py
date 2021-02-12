from math import log
from csv import DictReader
class mathOfId3:
    def __init__(self):
        # final out come label of main attribute
        self.mainAttributeLabel = []
        self.mainAttributeEntropy = float
        # final out come label of sub attributes of main attributes
      # sublabel contain a list of   
        self.subAttributeLabel = []
        self.subAttributeEntropy = []
        self.totalMain = -1      
        self.base = 0  
        self.averageInformationGainIs = 0
        self.informationGainIs = 0
    def setSubLabel(self,att):
        self.subAttributeLabel = att
    def setMainLabel(self,features):
        self.mainAttributeLabel = features
        self.base = len(features)
    def mainEntropy(self):
        """ 
        first find the total sum of the mainattribute list like [2,3]
        and total sum is 5 and find entropy and store it to main attribute entropy 
         """
        self.totalMain = self.countTotal(self.mainAttributeLabel)
        self.mainAttributeEntropy = self.entropy(self.mainAttributeLabel,self.totalMain)
    def subEntropy(self):
        """ find the subentropy attribute entropy and store it with its sum """
        t = 0
        for i in self.subAttributeLabel:
            t = self.countTotal(i)
            self.subAttributeEntropy.append([self.entropy(i,t),t])
    def countTotal(self,entropyList):
        """ it take input a list [4,2] 
        describtion of input:
        which contains the distinc number of labels final
        of a perticular attribute e.g sunny is an attribute and it come 6 time in a dataset
        and have 4 yes , 2 no final or answer labels
        task:
        add all the integers of the list and return it sum    
         
         """
        total = 0
        for i in entropyList:
            total += i    
        return total    
    def entropy(self,entropyList,total):
        """ 
        self.base : are the total number of distict main labels in dataset
        entropyList: contain total count of each attribute labels
        total: total of entropyList
        example entropyList =[1,2] its total count = 3 
        and base is 2 because this list give number of 2 distinc labels
        like 1 yes and 2 no 
        working:
        ratio: store the ratio of elements of entropyList and total e.g 1/3 from above example
        logOfRatio: store the log of ratio with the base - log of total with base
        entropy: multipulyRatio*withLogOfRatio and subtract it with the previous entropy 
        """
        ratio = 0
        logOfRatio = 0.0
        entropy = 0
        logT = log(total,self.base) 
        for j in entropyList:
            if j != 0:            
                ratio = j/total
                logOfRatio = log(j,self.base) - logT 
                entropy -= ratio*logOfRatio
        return entropy     

    def averageInformationGain(self):
        """ this function get the subAttribute entropy list which store
        [entropy,total] it simple divide the entropy with total number of labels
        of a column and multipuly with the total number of lables of main attributes
         """
        self.averageInformationGainIs = 0
        for j in self.subAttributeEntropy:
            self.averageInformationGainIs += (j[1]/self.totalMain)*j[0]
    def informationGain(self):
        self.informationGainIs =  self.mainAttributeEntropy-self.averageInformationGainIs
    def getInformationGainAndEntropys(self,mainAttribute,subAttribute):
        ''' 
        this class takes 2 main list arguments first is mainAttributeLabel
        
        mainAttributeLabel: 
        main attribute is a column name in dataset example outlook,temp etc int play_tennis dataset
        its labels are distict labels or answers in play_tennis example yes,no is the final label
        or conclusion of the dataset 
        mainAttributeLabel conatain the count of each distict labels or answers with respect to 
        that main label this count will be same for all the columns or main attributes
        because all share the same number of distict labels
        example play_tennis  contain 10 yes labels and 5 no labels so each column has
        5 no and 9 yes in then and these labels are store in the form of list [9,5]
        in mainAttributes which indicate that their are two main distict attributes one comes
        9 time and second one comes 5 time if their is third one you can add its count as well

        subAttributeLabel:
        sub attributes are the attributes of a perticular columns e.g sub attributes of 
        column name outlooks are sunny,overcast,rain these are the attributes of the attribute
        of main attributes of outlook column name
        labels labels of these attributes means number of distinct labels that comes against 
        each sub attributes e.g sunny has 2 yes label and 3 no labels and it comes 5 time
        in column outlook and rain has 3 yes and 2 no overcast has 4 yes only so the sub attribute
        list is generated like this [[2,3],[3,2],[4,0]]where first index is refers outlook, second
        rain ,third overcasts number of labels note the if we sum all of them like sum yes
        labels of each sun columns it should be equal to 9 which is the number of yes label
        in outlook column and no is 5 this is also the number of no label in outlook 
        '''

        self.subAttributeEntropy = []
        self.setMainLabel(mainAttribute)
        self.setSubLabel(subAttribute)
        self.mainEntropy()
        self.subEntropy()
        self.averageInformationGain()
        self.informationGain()
        return [self.informationGainIs,self.subAttributeEntropy]

class mainNodeOfId3:
    def __init__(self,indexList):
        self.subChilds = []
        self.indexList = indexList
        self.nodeType = 'main'
        self.nameLable = None
        self.entropy = None
    def setChild(self,child):
        self.subChilds.extend(child)
    def setNodeName(self,name):
        self.nameLable = name    
    def printNode(self):
        print('main node started :--------with name',self.nameLable)
        print('index list',self.indexList)
        print('node type :',self.nodeType)
        print('node name',self.nameLable)
        for child in self.subChilds:
            child.printNode()    
        print('main node ended :--------with name',self.nameLable) 
    def searchAnswerInInfromationTree(self,predictionDict):
        print('main prediction',self.nameLable)
        if predictionDict.__contains__(self.nameLable):
            name = predictionDict[self.nameLable]
            for child in self.subChilds:
                if child.nameLable==name:
                    return child.searchAnswerInInfromationTree(predictionDict)    
            return None        
        else:
            return None    

class subNodeOfId3:
    def __init__(self,nameLabel,childOfNode):
        self.childNode = childOfNode
        self.nodeType = 'sub'
        self.nameLable = nameLabel 
    def printNode(self):
        print('sub node started :--------with name',self.nameLable)
        print('node type :',self.nodeType)
        print('node name',self.nameLable)
        self.childNode.printNode()
        print('sub node ended :--------with name',self.nameLable)  
    def searchAnswerInInfromationTree(self,predictionDict):
        print('sub prediction',self.nameLable)        
        return self.childNode.searchAnswerInInfromationTree(predictionDict)
class leafNodeOfId3:
    def __init__(self,nameLabel):       
        self.nodeType = 'leaf'
        self.nameLable = nameLabel
    def searchAnswerInInfromationTree(self,predictionDict):
        print('main prediction',self.nameLable) 
        return self.nameLable
    def printNode(self):
        print('leaf node started :--------with name',self.nameLable) 
        print('node type :',self.nodeType)
        print('node name',self.nameLable)
        print('leaf node ended :--------with name',self.nameLable)        


class treeOfId3:
    def __init__(self,path,AnsName):
        self.dataList = []
        self.filePath = path
        self.label = AnsName
        self.math = mathOfId3()
        self.nodeGoingToBeProcessed = []
        self.mainAttribute = {}
        self.subAttribute = {}
        self.ignoreAttribute = []
        self.labelsTypeList = []
        self.informationGainAndSubEntropy = {}
        self.listForInformationGain = {}
        self.rootNode = None
        self.dominantNode = None
    def loadData(self):
        try:
            with open(self.filePath,'r') as ar:
                rea = DictReader(ar)
                for i in rea:
                    self.dataList.append(i)
        except Exception as e:
            self.dataList.clear()
            return False            
        if not self.dataList[0].__contains__(self.label):
            self.dataList.clear()
            return False
        else:
            self.ignoreAttribute.append(self.label)    
            return True 
    def initializeRootNode(self):
        l = [i for i in range(len(self.dataList))]
        self.rootNode = self.generateMainNode(l)
        for dic in self.dataList:
            if not self.labelsTypeList.__contains__(dic[self.label]):
                self.labelsTypeList.append(dic[self.label])
        # print(self.labelsTypeList)   
          
    def generateInformationTree(self):
        while self.nodeGoingToBeProcessed != []:
            self.processNode()
    def printTree(self):
        self.rootNode.printNode()        
    def processNode(self):
        node = self.nodeGoingToBeProcessed.pop()
        self.collectDataFromIndexList(node.indexList)
        self.generateProcessingListForInformationGainFunction()
        self.prepareInformationGainAndSubEntropy()
        self.dominantNode = self.selectGreaterInformationGain() 
        node.setNodeName(self.dominantNode)
        # print(" dominant node := ",self.dominantNode)
        sub = self.generateSubLabelWithEntropy(self.dominantNode)
        node.setChild(self.generateSubNodeList(sub))
        self.ignoreAttribute.append(self.dominantNode)
        

        # print(self.informationGainAndSubEntropy)    
        # print(self.mainAttribute)
        # print(self.subAttribute)
    def generateMainNode(self,indexList):
        main = mainNodeOfId3(indexList)
        self.nodeGoingToBeProcessed.append(main)
        return main
    def generateSubNodeList(self,subNodeDictList):
        subNodeList = []
        for nodeInfo in subNodeDictList:
            # print(nodeInfo)
            if nodeInfo['entropy'] == 0.0 and len(nodeInfo['label']) == 1:
                # print(nodeInfo['name'],' node generated')  
                # print(' leafe node created with label ',nodeInfo['label'][0]) 
                subNodeList.append(subNodeOfId3(nameLabel=nodeInfo['name'],
                childOfNode=leafNodeOfId3(nodeInfo['label'][0])))
            else:
                # print(nodeInfo['name'],' node generated')  
                # print(' main node created with index list',nodeInfo['indexList']) 
                subNodeList.append(
                    subNodeOfId3(nameLabel=nodeInfo['name'],
                    childOfNode=self.generateMainNode(nodeInfo['indexList']))
                )
        return subNodeList        

    def collectDataFromIndexList(self,indexList):
        self.mainAttribute = {}
        self.subAttribute = {}
        for index in indexList:
            for mainAtt,subAtt in self.dataList[index].items():
                if not self.ignoreAttribute.__contains__(mainAtt):
                    self.setMainLabelAttribute(mainAtt,subAtt)
                    self.setSubAttributes(subAtt,index,self.dataList[index][self.label])

    def setMainLabelAttribute(self,main,sub):
        if self.mainAttribute.__contains__(main):
            if not self.mainAttribute[main].__contains__(sub):
                self.mainAttribute[main].append(sub)
        else:
            self.mainAttribute[main] = [sub]                
    def setSubAttributes(self,sub,index,labelName):
        if self.subAttribute.__contains__(sub):
            self.subAttribute[sub]['indexList'].append(index)
            if self.subAttribute[sub]['label'].__contains__(labelName):
                self.subAttribute[sub]['label'][labelName] += 1
            else:
                self.subAttribute[sub]['label'][labelName] = 1
        else:
            self.subAttribute[sub] = {'indexList':[index],'label':{labelName:1}}                            
    def generateProcessingListForInformationGainFunction(self):
        self.listForInformationGain = {}
        for mainAtt,subLis in self.mainAttribute.items(): 
            subAttLabelList = []  
            mainAttLabel = None         
            for subAtt in subLis:
                subAttLabel = []
                for labelName in self.labelsTypeList:
                    if self.subAttribute[subAtt]['label'].__contains__(labelName):
                        subAttLabel.append(self.subAttribute[subAtt]['label'][labelName])
                    else:
                        subAttLabel.append(0)    
                subAttLabelList.append(subAttLabel) 
            mainAttLabel = subAttLabelList[0].copy()
            for labelsNum in range(1,len(subAttLabelList)):
                for i in range(len(mainAttLabel)):
                    mainAttLabel[i] += subAttLabelList[labelsNum][i] 
            self.listForInformationGain[mainAtt] = [mainAttLabel,subAttLabelList]       

    def prepareInformationGainAndSubEntropy(self):
        self.informationGainAndSubEntropy = {}
        for main,lis in self.listForInformationGain.items():
            self.informationGainAndSubEntropy[main] = self.math.getInformationGainAndEntropys(
                lis[0],lis[1]
            )
    def selectGreaterInformationGain(self):
        ig = -1
        dominantNode = None
        for key,value in self.informationGainAndSubEntropy.items():
            if ig < value[0]:
                ig = value[0]
                dominantNode = key
        return dominantNode        
    def generateSubLabelWithEntropy(self,dominantNode):
        dominatSubNodeEntropy = self.informationGainAndSubEntropy[dominantNode][1]
        dominatNodeSubAttList = self.mainAttribute[dominantNode]
        lis = []
        name = ''
        for index in range(len(dominatNodeSubAttList)):
            name = dominatNodeSubAttList[index]
            lis.append({
                'name':name,
                'entropy':dominatSubNodeEntropy[index][0],
                'indexList':self.subAttribute[name]['indexList'],
                'label':list(self.subAttribute[name]['label'])
                })
        return lis    
    def predict(self,predictionDict):
        print(self.rootNode.searchAnswerInInfromationTree(predictionDict))

   










t = treeOfId3('play_tennis.csv','play')
print(t.loadData())
# for i in t.dataList:
#     print(i)
t.initializeRootNode()   
t.generateInformationTree() 
# tree is going to be printed
print('tree is going to be printed \n\n')
#t.printTree()
t.predict({'outlook':'Rain','wind':'Weak'})
# print('gains \n',t.listForInformationGain)
# print('infogain \n',t.informationGainAndSubEntropy)
# print('sunAttr \n',t.subAttribute)
# l = {'yes':'ho','no':'hell'}
# print('dict list is \n',list(l))
#print(entropyThree(60,2,20))
#print(entropy(p,n))   
#print('log formula+++++++++++++++++') 
#print(entropyWithLogFormulas(p,n))
# print(log(9/5,e))
# t =  9*5
# print(log(t,2))
# print(log(9,2) + log(5,2))
# l = mathOfId3()
# l.setMainLabel([9,5])
# l.setSubLabel([[2,3],[3,2],[4,0]])
# l.mainEntropy()
# l.subEntropy()
# print(l.mainAttributeEntropy)
# print(l.subAttributeEntropy)
# l.averageInformationGain()
# print(l.averageInformationGainIs)
# l.informationGain()
# print(l.informationGainIs)
# print(l.getInformationGainAndEntropys([9,5],[[2,3],[3,2],[4,0]]))
