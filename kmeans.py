from csv import DictReader
import random 
from math import sqrt
class kMeans:
    def __init__(self,path,numberOfClusters):
        # load data from that file
        self.path = path
        # and store it in data list
        self.dataList = []
        # tells us how many clusters you want to made
        self.numberOfClusters = numberOfClusters
        # a unique name is assign to access a perticuler center 
        # its cluster and that name is store in centroidsName list
        # center points are store in centroids 
        # and clusters are store in cluster dic with the name of center
        # and list of index from the dataList 
        self.centroids = {}
        self.cluster = {}
        self.centroidsName = []
        # use to find smallest value or distance 
        self.setHighest = 9999
        self.readData()
        self.initializeCentroids()
# this function read data from file and store it into the dataList list   
    def readData(self):
        """ 
        read data from csv file and store it in dataList variable while converting values
        into double datatype
         """
        try:
            with open(self.path,'r') as re:
                r = DictReader(re)
                print(' read ')
                d = {}
                for data in r:
                    d = {}
                    for i,j in data.items():
                         d[i] = float(j)
                    self.dataList.append(d)          
        except Exception as e:
            print(e)   
    def initializeCentroids(self):
        '''
        working:
            numberOfClusters:
                this class variable store the number of clusters which this algorithm 
                make from the current dataset
            dataList:
                dataList is a dictinary which store the copy of complete dataset from the
                file path define in self.path variable this dataList is filled in readData
                function
            for a single center point:
                this function allocate a unique name to that perticular center and save
                this name to the centriodsName which make it easy for other methods to use 
                centriods
                it use a random function and chose a random
                datatuple or dictionary from the dataList variable and set is as a center for
        '''
        name = None
        for i in range(self.numberOfClusters):
            name = f'c{i}'
            self.cluster[name] = [] 
            self.centroids[name] = self.dataList[random.randint(0,len(self.dataList)-1)].copy()
            self.centroidsName.append(name)


    def makeNewCenters(self):
        '''
        addDataSet:
            centroids are taken from the dataset so their dict keys are same {'V1':3,'V2':2,...}
            this method add similar key values of a dict and store result in a center dict
            example
            if their is one dataTuple {'v1':2,'v2':8} and center {"v1":9,"v2":5}
            the new center shall be
            {"v1":11,"v2":13} after addDataSet Function
        meanOfCenter:
            this method divide each key value with the dataList length
        isEqual:
            this method compare each key value with the other center and return true
            if all the key values are equal
        working:
            this method traverse all the clusters of the centers
            for each cluster:
                this method first initialize a new center with the first data value
                of the cluster with the key name of cluster which is the name of 
                the previous center by pop method which discard the first
                data member from the index list
                for each dict value of cluster's index list:
                    this method add all the data dict with the new center by using addDataSet
                    method and in such a way the each element in the index list is poped
                    after adding it to the new cluster
                then use meanOfCenter method to store means in the center
                compare previous and new centers
                make class center equal to new center
                return the compared booloean value    
        '''
        def addDataSet(center,data):
            for i,j in data.items():
                center[i] += j
            return center     
        def meanOfCenter(center,length):
            for i in center:
                center[i] = center[i]/length
            return center        
        def isEqual(nCenters):
            for key,center in nCenters.items():    
                for i,j in center.items():
                    if self.centroids[key][i] != j:
                        return False
            return True        
        lengthOfAttributes = len(self.dataList[0])  
        similarCentroids = True
        currentCenter = None
        newCenter = {}
        le = 0
        for key,indexList in self.cluster.items():
            if indexList != []:
                le = len(indexList)
                newCenter[key] = self.dataList[indexList.pop()].copy()
                for i in range(len(indexList)):
                    addDataSet(newCenter[key],self.dataList[indexList.pop()])
                meanOfCenter(newCenter[key],le)  
            else:
                newCenter[key] = self.dataList[random.randint(0,len(self.dataList)-1)].copy()    
        similarCentroids = isEqual(newCenter)
        print('is equal ',similarCentroids)
        print('old center',self.centroids)
        print('new centers',newCenter)
        self.centroids = newCenter           
        return similarCentroids             
# this function use arcadian distance function which return distance between two points
# or dictionarys this function will include the index of a perticular tuple to
# the center which have the lowest distance amoung all the centers that are define  
    def setCentroidsIndexList(self):
        '''
        distance:
            this variable is use to find out the smallest arcadian distance between 
            a center and a datatuple of dataSet 
        working:
            this function traverse all the dataList
            for a single tuple or dict:
                it traverse all the centers with their names and find arcadian distance
                between a center and a perticular data tuple and store the center name
                and arcadian distance which gives smallest distance value
                on start of the next iteration:
                    it appent that dataTuple index in the cluster self.cluster
                    list of that center which gives smallest distance 
                self.cluster:
                    is a cluster dict with the name of the centroid as a key
                    and list of cluster as a value
                self.centroids:
                    is a dict which contain a random data tuple from the data list first
                    and than keep changing as the program proceed
                self.centroidsName:
                    contain the name of centroids to make it easy to access both
                    centroids tuple and their cluster            
        '''
        distance = self.setHighest
        # print('d is',d)
        data = None
        centroidSelected = self.centroidsName[0]
        for index in range(len(self.dataList)):
            data = self.dataList[index]
            for center in self.centroidsName:
                arca = self.calculateArgadianDistance(self.centroids[center],data)
                print("arcadia distance of center :",center," data is: ",data," arcadian distance: ",arca) 
                if distance > arca:
                    distance = arca
                    centroidSelected = center
            self.cluster[centroidSelected].append(index)
            distance = self.setHighest
        print(" centers :  ",self.centroids)    
        print('cluster is \n',self.cluster)        
# this function will keep running the makeNewCenter function and setCentriodsIndexList 
# function untill the makeNewCenter return True
    def findTrueCenters(self):
        """
        working:
            this method first generate clusters of centriods by using setCentroidsIndexList
            method and than make new centers by using makeNewCenters method and it will
            run until makeNewCenters return true which symbolise the previous centers are equal
            to the newCenters 

        """
        print('random number')
        print("centers : ",self.centroids)
        print('initialize')
        self.setCentroidsIndexList()
        print('while start')
        a = 0
        while not self.makeNewCenters():
            self.setCentroidsIndexList()
            print('iteration ',a)
            a += 1
     
# calculate distance between two points which are accually dict with same keys
#  in this case
    def calculateArgadianDistance(self,dis1,dis2):
        '''
        working:
            this method use arcadian distance formula
            sqrt of (x1-x2)^2 + (y1-y2)^2 + (z1-z2)^2 ...
            in above example x1 belong to one point or data tuple and x2 belong
            to second data tuple 
            in this program x1,x2,.. are the keys and values of a dict 
        '''
        distance = 0
        totalDistance = 0
      #  print("dist1: ",dis1," dist2: ",dis2)
        for i,j in dis1.items():
            distance = dis2[i] - j
            distance *= distance
            totalDistance += distance
        # print(totalDistance)    
        return sqrt(totalDistance)
# return the center with minimum distance  
    def predict(self,dataTuple):
        def isEqual():
            return list(dataTuple).__eq__(list(self.dataList[0]))
        if isEqual():
            distance = self.setHighest
            d = 0
            selectedName = None
            for i,j in self.centroids.items():
                d = self.calculateArgadianDistance(dataTuple,j)
                if distance > d:
                    distance = d
                    selectedName = i
            return {'smallestDistance':distance,
            'centerName':selectedName,
            'center':self.centroids[selectedName]}        




    



k = kMeans('dara.csv',2)
k.findTrueCenters()
#print(k.predict(k.dataList[10]))
#k.setCentroidsIndexList()
# print(k.cluster)
# k.makeNewCenters()
#print(k.readData())
