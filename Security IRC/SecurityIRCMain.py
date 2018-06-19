# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 19:57:04 2017

This program starts by building a Neural Network that takes in 128 bits as input 
and 24 bits as output. There's a hidden layer of 256 (responsible for making the decisions
for output). The Neural netowrk then trains on the test data given 128 bits and 24 bits (so it 
recognizes what the output should be). Afterwards, the user is given control of commands to
train the neural network, test (given a test data file), If the test command is run, the neural 
network runs tests on the given file and then predicts what the binary form of the password is.
Checks are then applied to see how close the predictions are.

@author: Andrew Buxa
"""

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import matplotlib.pyplot as plt

"Builds network"
net = buildNetwork(128,256,24,bias=True)
"Builds training set"
ds = SupervisedDataSet(128,24)
enabled = True
maxBits = 24
file = open("testDataConv.txt","r")

for line in file:
    snippet = line.split(' ')    
    hashPass = snippet[0].rstrip('\n')
    charPass = snippet[1].rstrip('\n')
    hashArray = []
    charArray = []
    # Add 0's and 1's from the 128-bit hashed password into an array as input for
    # the Neural Network training phase.
    for index in hashPass:
        hashArray.append(index)
    # Add 0's and 1's from the 24-bit hashed password into an array as input for
    # the Neural Network training phase.
    for index in charPass:
        charArray.append(index)
    
    ds.addSample(hashArray,charArray)

trainer = BackpropTrainer(net,ds)
trainer.train()


"""
This function caluclates the hamming distance between two given sequences.
Hamming distance is the number of changes that must be made to turn one 
sequence into another sequence. Then, the function returns the distance.

seq1 = Actual Password
seq2 = Neural Net Prediction
"""
def hammingDistance(seq1, seq2):
    distance = 0
    greaterLength = 0
    sequenceOneLength = len(seq1)
    sequenceTwoLength = len(seq2)
    if seq1 == seq2:
        return 0
    if sequenceOneLength >= sequenceTwoLength:
        greaterLength = sequenceOneLength
    else:
        greaterLength = sequenceTwoLength
    
    for index in range(greaterLength):
        try:        
            if seq1[index] != seq2[index]:
                distance = distance + 1
        except IndexError:
            break
    distance = distance + abs(sequenceOneLength - sequenceTwoLength)
    return distance

"""
while loop that accepts user input 
(Either a file name to load data or exit command)
"""
resultFile = open("trainDataConv.txt","w")
while(enabled):
    "Do things"
    choice = input("Please enter in what you would like to do: \n train \n test \n accuracy \n exit \n")
    if (choice.lower() == "exit"):
        enabled = False
       
    if (choice.lower() == "train"):
        trainer.train()
    
    if (choice.lower() == "test"):
        withinArray = [0]*maxBits
        inCountArray = [0]*maxBits
        fileName = input("Please enter the name of your data file (excluding .txt): \n")
        testFile = open(fileName+".txt","r")
        correct = 0 #Number of correct 100% predictions
        wrong = 0 # Number of wrong predictions
        counter = 0 # Counter to keep track of how many sets of test data there are.
        resVal = 0 # total residual value for the entire test set.
       
        
        # Iterate over input file to acquire output from the Neural Network
        # to get the prediction and compare it to the actual password and 
        # check for accuracy.
        for line in testFile:
            data = line.split(' ')
            digest = data[0].rstrip('\n')
            characterPass = data[1].rstrip('\n')
            digestArray = []
            transformedPass = ""
            for index in digest:
                digestArray.append(index)
            # Get 24-bit prediction from the Neural Network.
            output = net.activate(digestArray)
            
            counter+=1
            # Checks the array of 24 floats the Neural Network outputs
            # to determine whether the float should be a 0 or 1.
            for character in output:
                if (float(character) < 0.5):
                    transformedPass += "0"
                else:
                    transformedPass += "1"
                    
            resValArray = []
            resIndexArray = []
            # Calculating the Residual Value of each element in the 24-bit array
            # returned from the Neural Network, then add each value into one
            # score for accuracy.
            for index in range(len(output)):
                tempPredVal = output[index]
                resValArray.append(abs(int(transformedPass[index]) - tempPredVal))
                resVal += abs(int(transformedPass[index]) - tempPredVal)
                resIndexArray.append(index)
                
            # Sorting the array of residual values from lowest (least confident)
            # to highest (most confident)
            # Need to keep track of the indicies as well.
            sortedValArray = []
            sortedIndexArray = []
            for index in range(len(resValArray)):
                sortedValArray.append(abs(0.5 - resValArray[index]))    
            sortedValArray.sort()
            
            # Sorted value array finding the new indices of the values compared
            # to the origninal ones
            
            for index in range(len(sortedValArray)):
                changedVal = abs(0.5 - resValArray[index])
                sortedIndexArray.append(sortedValArray.index(changedVal))
                changedVal = 0
            
            #Iterate through the sorted value array and make changes in each position
            # bigger the number, farther from median you are
            # character = "000001010100010"
            # output [0.23,0.54,0.1,0.84.....]
            #transformed pass [0 0 0 0 1 1 0 1]
            #sorted index array [0 5 3 9 1 8 5  2 7]
            # see if each index matches the other up until the furthest point where the index/values don't match
            # for example, up to the 9th spot in sorted list needs to be changed
            lenToChange = 0
            for index in range(len(output)):
                if (characterPass[index] != transformedPass[index]):
                    lenToChange = index
            
            withinArray[sortedIndexArray.index(lenToChange)]+=1

            
                    
            
            # Check to see if the predicted password (converted into 0's or 1's) 
            # is 100% identical to the actual password, if so, correct++ otherwise,
            # wrong++
            if (characterPass == transformedPass):
                correct+=1
            else:
                wrong+=1
                
        
    if (choice.lower() == "accuracy"):
        print("Out of "+str(counter)+" passwords")
        print("Predictions that are wrong: "+str(wrong))
        print("Out of "+str(2**len(charPass))+" possible combinations")
        print("_____________________________________________________________________")
        print("0 flips needed: "+str(correct)+" --- 0 possible changes (2^0)")   
        print("1 flips needed: "+str(withinArray[0])+" "+"("+"{0:.2f}".format(withinArray[0]/counter*100)+"%"+")"+" --- 2 possible changes (2^1)")
        print("2 flips needed: "+str(withinArray[1])+" "+"("+"{0:.2f}".format(withinArray[1]/counter*100)+"%"+")"+" --- 4 possible changes (2^2)")
        print("3 flips needed: "+str(withinArray[2])+" "+"("+"{0:.2f}".format(withinArray[2]/counter*100)+"%"+")"+" --- 8 possible changes (2^3)")
        print("4 flips needed: "+str(withinArray[3])+" "+"("+"{0:.2f}".format(withinArray[3]/counter*100)+"%"+")"+" --- 16 possible changes (2^4)")
        print("5 flips needed: "+str(withinArray[4])+" "+"("+"{0:.2f}".format(withinArray[4]/counter*100)+"%"+")"+" --- 32 possible changes (2^5)")
        print("6 flips needed: "+str(withinArray[5])+" "+"("+"{0:.2f}".format(withinArray[5]/counter*100)+"%"+")"+" --- 64 possible changes (2^6)")
        print("7 flips neededt: "+str(withinArray[6])+" "+"("+"{0:.2f}".format(withinArray[6]/counter*100)+"%"+")"+" --- 128 possible changes (2^7)")
        print("8 flips needed: "+str(withinArray[7])+" "+"("+"{0:.2f}".format(withinArray[7]/counter*100)+"%"+")"+" --- 256 possible changes (2^8)")
        print("9 flips needed: "+str(withinArray[8])+" "+"("+"{0:.2f}".format(withinArray[8]/counter*100)+"%"+")"+" --- 512 possible changes (2^9)")
        print("10 flips needed: "+str(withinArray[9])+" "+"("+"{0:.2f}".format(withinArray[9]/counter*100)+"%"+")"+" --- 1,024 possible changes (2^10)")
        print("11 flips needed: "+str(withinArray[10])+" "+"("+"{0:.2f}".format(withinArray[10]/counter*100)+"%"+")"+" --- 2,056 possible changes (2^11)")
        print("12 flips needed: "+str(withinArray[11])+" "+"("+"{0:.2f}".format(withinArray[11]/counter*100)+"%"+")"+" --- 4,096 possible changes (2^12)")
        print("13 flips needed: "+str(withinArray[12])+" "+"("+"{0:.2f}".format(withinArray[12]/counter*100)+"%"+")"+" --- 8,192 possible changes (2^13)")
        print("14 flips needed: "+str(withinArray[13])+" "+"("+"{0:.2f}".format(withinArray[13]/counter*100)+"%"+")"+" ---  16,384 possible changes (2^14)")
        print("15 flips needed: "+str(withinArray[14])+" "+"("+"{0:.2f}".format(withinArray[14]/counter*100)+"%"+")"+" ---  32,768 possible changes (2^15)")
        print("16 flips needed: "+str(withinArray[15])+" "+"("+"{0:.2f}".format(withinArray[15]/counter*100)+"%"+")"+" --- 65,536 possible changes (2^16)")
        print("17 flips needed: "+str(withinArray[16])+" "+"("+"{0:.2f}".format(withinArray[16]/counter*100)+"%"+")"+" --- 131,072 possible changes (2^17)")
        print("18 flips needed: "+str(withinArray[17])+" "+"("+"{0:.2f}".format(withinArray[17]/counter*100)+"%"+")"+" --- 262,144 possible changes (2^18)")
        print("19 flips needed: "+str(withinArray[18])+" "+"("+"{0:.2f}".format(withinArray[18]/counter*100)+"%"+")"+" ---  525,288 possible changes (2^19)")
        print("20 flips needed: "+str(withinArray[19])+" "+"("+"{0:.2f}".format(withinArray[19]/counter*100)+"%"+")"+" --- 1,048,576 possible changes (2^20)")
        print("21 flips needed: "+str(withinArray[20])+" "+"("+"{0:.2f}".format(withinArray[20]/counter*100)+"%"+")"+" ---  2,097,152 possible changes (2^21)")
        print("22 flips needed: "+str(withinArray[21])+" "+"("+"{0:.2f}".format(withinArray[21]/counter*100)+"%"+")"+" --- 4,194,304 possible changes (2^22)")
        print("23 flips needed: "+str(withinArray[22])+" "+"("+"{0:.2f}".format(withinArray[22]/counter*100)+"%"+")"+" ---  8,388,608 possible changes (2^23)")
        print("24 flipped bits correct: "+str(withinArray[23])+" "+"("+"{0:.2f}".format(withinArray[23]/counter*100)+"%"+")"+" ---  16,777,216 possible changes (2^24)")   
        print("_____________________________________________________________________")
        perArray = [0]*maxBits
        for index in range(len(withinArray)):
            perArray[index] = "{0:.2f}".format(withinArray[index]/counter*100)
        plt.plot(perArray, '.b-')
        plt.axis([0,len(withinArray),0,counter/counter*100])        
        plt.ylabel('Fraction of Passwords')
        plt.xlabel('Number of flipped bits')
        plt.show()
        
resultFile.close()
testFile.close()