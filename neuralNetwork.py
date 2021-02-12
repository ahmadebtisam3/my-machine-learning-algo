from random import uniform
from math import e
class network:
    def __init__(self):
        self.networkList = []
        self.inputLayer = None
        self.aspectedLayer = None
        self.min = 0.0
        self.max = 1.0
        self.alpha = 0.1
        self.weightLayer = None
    def setAlpha(self,alpha):
        self.alpha = alpha    
    def buildNetwork(self,neuronsList,InputLayer,AspectedLayer,weightLayersList = []):
        """ 
        buildNetwork takes three list argunemts 
        neuronsList: 
            takes the of number of neurons for a each layers that come after input layer
            e.g the number at 0th index is the number of neuron of the second layer that come after inputlayer
        InputLayer:
            take the list of inputs that are going to be passed in neuralNetwork
        AspectedLayer
            is the output layer which is use to calculate errors in neural network   
        weightLayersList:
            is an optional argument it will take the list of weights . weight must be compatable with the
            given structure of network of not then it will use random function and make weights it self
            makeWeightLayer function    
        """
        self.networkList.append(self.makeLayer(len(InputLayer)))
        for neuronsNumber in neuronsList:
            if weightLayersList != []:
                self.weightLayer = weightLayersList.pop(0)  
            self.addLayer(neuronsNumber) 
        if weightLayersList != []:
            self.weightLayer = weightLayersList.pop(0)                  
        self.addLayer(len(AspectedLayer)) 
        self.setInputAndAspectedLayer(InputLayer,AspectedLayer)      

    def setInputAndAspectedLayer(self,newInputLayer,newAspectedLayer):
        """
        run the same build neural network with new inputs and aspected Layer's data
        """
        l = len(self.networkList[len(self.networkList)-1])
        if (len(self.networkList[0]) == len(newInputLayer)) and (l == len(newAspectedLayer)):
            self.inputLayer = newInputLayer
            self.aspectedLayer = newAspectedLayer
            for num in range(len(newInputLayer)):
                self.networkList[0][num][1] = newInputLayer[num]


    def addLayer(self,numberOfNeurons):
        '''
        numberOfNeurons: 
            this parameter is use to pass this parameters to makeLayer method which make the neuron layer
            and this method addLayer add new layer to the network
        addLayer: 
            means adding a layer after inputLayer so it is nessessary to have input layer in network
            working:
                before adding the new layer it add a weight layer with the size of addingLayer*sizeOfPrevious layer
                this weight layer is large enough to make connection between previous layer in the network with the 
                newly adding layer and than add the new layer to the network
        '''
        if len(self.networkList) > 0:
            previousLayerLength =  len(self.networkList[len(self.networkList)-1])
            self.networkList.append(self.makeWeightLayer(numberOfNeurons,previousLayerLength))
            self.networkList.append(self.makeLayer(numberOfNerurons=numberOfNeurons))  
    def makeWeightLayer(self,previousLayerLength,currentLayerLength):
        """ 
        previousLayerLength:
            is the size of the last layer in the network 
        currentLayerLength:
            is the size of the neuron's layer which is going to be added after adding this 
            weight layer which is created by and returned by this makeWeightLayer method
        working:
                this method make a list of uniform random fraction double numbers between 0.0 to 1.0 
                of size equal to previousLayerLength*currentLayerLength and return this list
        """
        if self.weightLayer:
            if len(self.weightLayer) == previousLayerLength*currentLayerLength:
                return self.weightLayer
        weightLayer = []
        for i in range(previousLayerLength*currentLayerLength):
            weightLayer.append(round(uniform(self.min,self.max),4))
        return weightLayer    

    def makeLayer(self,numberOfNerurons):
        """
        numberOfNeurons:
            is the size of neurons layer which this method returned
        working:
            a new neurons layer is made by adding neurons 
            neuron:
                a neuron consist on a list containing two value [error,output] 
                the value at 0th index of neuron is error of neuron and
                at 1th index of neuron is its output value
            this method add neurons [error,output] to a layer and make this layer
            equal to the size of numberOfNeurons parameter and return the layer 2d list     

        """
        layer = []
        for i in range(numberOfNerurons):
            layer.append([0,0])
        return layer    
    def printNetwork(self):
        print(" printing network ")
        for i in self.networkList:
            print(i,len(i))
        print(" network ended ")    
    
    def networkPrediction(self):
        """
        working:
            this method use to three for loop first loop iterate the network which is design like layer,weight,layer
            networkPattren:
                output layer:
                the first layer is the outputlayer which is use to ouput
                weight between both layers:
                then the weight layer which is equal to the size of the product of both layers
                input Layer:
                the second layer is the input layer which is using the output of previous layer
            this algorithm use the above defined layer patteren to implement the neural network
            layerNumber is the output layer index:
                first loop will always give the output layer index because every layer after weight layer can
                be output layer or inputlayer but we conside the variable layerNumber index as a output layer index
            layerNumber+1 is the weight layer index:
                after every input layer their is a weight layer which is in between input and out layer with the size
                of inputLayer*outputLayer
            layerNumber+2 is the outputLayer 
                after weight layer their comes the output layer which will recived input from the inputLayer via weight layer   

            algorithm:
                as we know our layer pattern every output layer have a weight layer which place one index before it
                so the weight layer connects the output layer to the input layer in such a way that a single node of
                output layer is connected with the whole input layer with its unique weight
                e.g
                outputLayer = [[0,2],[0,3]]
                weight = [1,2,3,4,5,6] -> 2*3 size of inputLayer*outputLayer        
                inputLayer = [[0,5],[0,1],[0,8]]
                so the output layer [0,2] node is connected by the whole input layer with unique weights
                [0,2] -> 1 -> [0,5]
                [0,2] -> 2 -> [0,1]
                [0,2] -> 3 -> [0,8]
                similarly second one is
                [0,3] -> 4 -> [0,5]
                [0,3] -> 5 -> [0,1]
                [0,3] -> 6 -> [0,8]
            math:
                first loop will give the output layer
                counter of weight is set to zero
                second nested loop will iterate the outputLayer    
                and then third nested loop will iterate input layer
                thus making the same condition as describe above
                then single node of input layer is multipulyed by its respective weight and added in the
                outputLayes output index 
                in above example
                [0,2] -> 1 -> 2*1 -> [0,5+2]->[0,7]
                [0,2] -> 2 -> 2*2 -> [0,1+4]->[0,5]
                [0,2] -> 3 -> 2*3 -> [0,8+6]->[0,14]
                similarly 
                [0,3] -> 4 -> 3*4 -> [0,7+12]->[0,19]
                [0,3] -> 5 -> 3*5 -> [0,1+15]->[0,16]
                [0,3] -> 6 -> 3*6 -> [0,8+18]->[0,26]
                so after execution the output layers output shall be
                [0,19]
                [0,16]
                [0,26]
                then sigmoid function is applied to each node to turn this result in in between zero and 1
            after that this output layer is consider as input layer and another outputlayer is loaded
            and its output is calculated and so on     
        """
        networkLength = len(self.networkList)
        outputValue = inputValue = weightValue = 0
        for layerNumber in range(0,len(self.networkList),2):
            weightCounter = 0
            if layerNumber <= networkLength-2:
                for outputLayer in self.networkList[layerNumber]:
                    for inputLayer in self.networkList[layerNumber+2]:
                        outputValue = outputLayer[1]
                        weightValue = self.networkList[layerNumber+1][weightCounter]
                        inputLayer[1] += outputValue*weightValue
                        weightCounter += 1 
                self.sigmoidFunctionOnALayer(self.networkList[layerNumber+2])                                                   
    def sigmoidFunctionOnALayer(self,layer):
        for node in layer:
            node[1] = round(self.sigmoindFunction(node[1]),4)
    def sigmoindFunction(self,value):
        return round((1/(1+pow(e,-value))),2)
    def networkErrorCorrection(self):
        """
        this start traversing network from second last layer of the network to the first layer of the network in
        layer structure as describe in networkPrediction method (inputLayer weight outputLayer) but
        in this case outputLayer becomes errorLayer because we are dealing with thr errors
        this time instead of dealing with the output of a node its deals with the error of the node
        base error is already calculated by the resultErrorCorrection method then neural network formula is
        use to calculate error of
        first a single node of input layer at zero index store the sum of all the errorLayer node multiply by
        connected weight between that perticular node of input layer and error layer 
        e.g
        [0,4] 5,6,9,8 [2,9],[3,8]
        in this case we will deal with the left side at 0th index which is error index
        [0,4]->5->[2,9]->5*2->[10,4]
        [10,4]->6->[3,8]->6*3->[28,4]
        similarly is will done this to every node of the inputLayer
        before going to the next node of input layer algo applied the error formula
        which is 
        (inputLayer'sValue)*(1-inputLayer'sValue)*(sum of (the product of weight and errors) 
        between inputLayer node and error layer )
        """
        self.resultErrorCorrection()
        for layerNumber in range(len(self.networkList)-3,-1,-2):
            weightCounter = 0
            if layerNumber >= 0:
                for inputLayer in self.networkList[layerNumber]:
                    inputLayer[0] = 0
                    for errorLayer in self.networkList[layerNumber+2]:
                        inputLayer[0] += self.networkList[layerNumber+1][weightCounter]*errorLayer[0]
                        self.networkList[layerNumber+1][weightCounter] +=round(errorLayer[0]*self.alpha*inputLayer[1],4)
                        weightCounter += 1
                    inputLayer[0] = (inputLayer[1])*(1-inputLayer[1])*inputLayer[0]    
                    inputLayer[1] = 0    

    def resultErrorCorrection(self):
        result = self.networkList[len(self.networkList)-1]
        counter = 0
        for node in result:
            error = node[1]*(1-node[1])*(self.aspectedLayer[counter]-node[1])
            node[0] = round(error,4)
            node[1] = 0
            counter += 1

net = network()
net.buildNetwork([2,3],[8],[0,1,0],[[0.1,0.2],[0.1,0.2,0.3,0.4,0.5,0.6],[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]])
net.printNetwork()
print("forword")
net.networkPrediction()
net.printNetwork()
net.networkErrorCorrection()
net.printNetwork()





