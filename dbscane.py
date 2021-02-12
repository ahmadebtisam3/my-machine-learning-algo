from csv import DictReader
from math import sqrt
class densityBaseClustring:
    def __init__(self,path):
        self.path = path
        self.distanceBetweenPoints = {}
        self.dataList = []
        self.pointStatus = ['core','border','noise']
        
    def readData(self):
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
    def findDistanceBetweenPoints(self):
        '''
        this method will find arcadian distance between one data point and the entire 
        dataList . And store it to the self.distanceBetweenPoints dict with the key
        as an index of that point in the list and value is the list of index of other
        point and arcadian distance between them
        working:
            this method use two for loop
            first loop:
                will start from 0 to last index of the dataList
                second loop:
                    will start from index of the first loop to the last called as index2
                with these loops arcadian distance is found between index and index2
                and use self.addTwoIndexAndDistance method to store result in distanceBetweenPoint
                dict
        '''
        data = None
        data2 = None
        for index in range(len(self.dataList)):
            data = self.dataList[index]
            for index2 in range(index,len(self.dataList)):
                data2 =  self.dataList[index2]
                arca = round(self.calculateArgadianDistance(data2,data),4)
                self.addTwoIndexAndDistance(index,index2,arca)
    def addTwoIndexAndDistance(self,index1,index2,distance):
        if index1 != index2:
            self.addPointsInDistancePointDict(index1,index2,distance)
            self.addPointsInDistancePointDict(index2,index1,distance)            
    def addPointsInDistancePointDict(self,index1,index2,distance):
        '''
        this method use index1 as a key and append index2 and distance in the list
        of index1 as a value if key not exist create a new list with index and distance
        list
        '''
        if not self.distanceBetweenPoints.__contains__(index1):
            self.distanceBetweenPoints[index1] = [[index2,distance]]
        else:
            self.distanceBetweenPoints[index1].append([index2,distance])    

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

    def findPointStatus(self,index,minimumPoints,ranges):
        '''
        this method traverse the list of index from the self.distanceBetweenPoints dict and
        store only index in points and return points with condition of state
        if number of points >= minumPoints status will be core
        if less than and greater than 1 than border else noise point 
        range:
            is use to select points with smaller or equal arcadian distance selected dataPoint
            store in points list
        '''
        points = []
        if self.distanceBetweenPoints.__contains__(index):
            points.append(index)
            for pointsIndexWithDistance in self.distanceBetweenPoints[index]:
                if pointsIndexWithDistance[1] <= ranges:
                    points.append(pointsIndexWithDistance[0])
        totalpoints = len(points)
        if totalpoints >= minimumPoints:
            return [self.pointStatus[0],points]
        elif totalpoints < minimumPoints and totalpoints > 1:
            return [self.pointStatus[1],points]
        return [self.pointStatus[2],points]                        
    def findAllPointsStatus(self,minimumPoints,ranges):
        ''' 
        traverse all the self.distanceBetweenPoints dict and use self.findPointStatus
        to find the status of a pertucular point and store it result in a dict
         '''
        pointsStatusList = {}
        for index in self.distanceBetweenPoints:
            pointsStatusList[index]= self.findPointStatus(index,minimumPoints,ranges)
        return pointsStatusList    
    def makeCluster(self,minimumPoints,ranges,indexList:list,allpointstatus):
        '''
        indexList:
            is the list of indexes from which cluster shall be made
        allpointstatus:
            use allpointsStatus method to find out all the status of the points

        this method create cluster of all those points that are connected with
        each other 
        cluster:
            is made by popping an element from the stack
        and the stack is filled by by pushing first element of the indexList    
        in just first iteration   
        and than pushing all the points in allpointsstatus dict of popped point from the stack
        to the stack which are not avalable in indexList the pushed point is also 
        removed from the index list this process is performed untill stack become empty
        as a result all the connected points are gather in a single cluster and those
        points that are not connected shall remain in the indexList 
        '''
        indexStack = []
        cluster = []
        indexStack.append(indexList.pop(0))
        currentIndex = None
        while indexStack != []:
            currentIndex = indexStack.pop(0)
            cluster.append(currentIndex)
            for indexl in allpointstatus[currentIndex][1]:
                if indexList.__contains__(indexl):
                    indexStack.append(indexl)
                    indexList.remove(indexl)
        return [cluster,indexList]
    def makeAllClusters(self,minimumPoints,ranges):
        '''this method call makecluster method untill indexList become empty thus making all
        the clusters in a dataset form by specified minimumPoint and range'''
        indexList = [i for i in range(len(db.dataList))]
        clusters = []
        temp = None
        allpointstatus = self.findAllPointsStatus(minimumPoints,ranges)
        while indexList != []:
            temp = self.makeCluster(minimumPoints,ranges,indexList,allpointstatus)
            indexList = temp[1]
            clusters.append(temp[0])
        return clusters            





db = densityBaseClustring("dataset.csv")
db.readData()
db.findDistanceBetweenPoints()
# for i,j in db.distanceBetweenPoints.items():
#     print("point no ",i," ",db.dataList[i])
#     for points in j:
#         print(points)
#print(db.findPointStatus(1,3,2.5))
# for po,index in db.findAllPointsStatus(3,2.5).items():
#     print(po)
#     print(index)
#print(db.makeCluster(3,2.5,[i for i in range(len(db.dataList))]))
print(db.makeAllClusters(3,2.5))