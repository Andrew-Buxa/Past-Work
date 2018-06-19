# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 11:02:33 2016

@author: Andrew Buxa
"""
import collections
import random as rand
import math
import time


nucFreqs = {}
"""
This function just accepts the name of a file then reads in the lines of that file and save it into a list.

fileName - Name of the file to be read from
""" 
def readInput(fileName):
    sequenceFile = open(fileName+".txt").readlines()
    sequenceList = []
    for i in range(len(sequenceFile)):
        sequenceList.append(sequenceFile[i].strip())
    return sequenceList

"""
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\Randomized Motif Search for IRC///////////////////////
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
"""
"""
This function takes in possible motifs which is a list of "motifs" that must be converted to a profile matrix, then scored in order to determine whether they are
actual motifs. Taken from Chapter 2 of the Bioinformatics book.

possibleMotifs - List which contains strings of supposed "motifs"

"""
def score(possibleMotifs):
	score = 0
	consensus = consensusSeq(possibleMotifs)
	for index in possibleMotifs:
		score = score + hammingDistance(consensus, index)
	return score

"""
This function caluclates the hamming distance between two given sequences.
Hamming distance is the number of changes that must be made to turn one 
sequence into another sequence. Then, the function returns the distance.

seq1 = First DNA sequence
seq2 = Second DNA sequence
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
This function takes in a matrix of "possible motifs" and returns the most common 
letters in each column of the sequence.

motifs = matrix of a motif
"""
def consensusSeq(motifs):
    consensus = ''
    count = {}
    
    for index in range(len(motifs[0])): #Runs through the length of sequences
        count['A'] = 0
        count['C'] = 0
        count['T'] = 0
        count['G'] = 0
        for motif in motifs: # Runs through the characters in each sequence
            count[motif[index]] = count[motif[index]] + 1
            
        consensus+= max(count, key=count.get) # Grabs the key with the highest value
    
       
    return consensus
"""
Returns a number between 1 and a given length, used as a helper function.

"""
def randomNum(n):
    return rand.randint(0,n)
"""
Randomly select k-mers Motifs = (Motif_1, ... , Motif_t) in each string from Dna
BestMotifs <- Motifs
while forever
Profile <- Profile(Motifs)
Motifs <- Motifs(Profile, Dna)
if Score(Motifs) < Score(BestMotifs)
    BestMotifs <- Motifs
else:
    return BestMotifs
"""
"""

dna = dna sequence
k = k-mer size to find the best scoring motif
l = length of the dna sequence
"""
def randomizedMotifSearch(dna, k):
    bestMotifs = []
    motifs = []
    iterations = 1000
    count = 0
    for index in range(0,len(dna)):
            ranNum = randomNum(len(dna[index]) - k)
            if ranNum + k > len(dna[index]):
                break
            else:
                bestMotifs.append(dna[index][ranNum:ranNum+k])
    bestMotifScore = score(bestMotifs)
    while count <= iterations:
        motifs = []
        for index in range(0,len(dna)):
            ranNum = randomNum(len(dna[index]) - k)
            if ranNum + k > len(dna[index]):
                break
            else:
                motifs.append(dna[index][ranNum:ranNum+k])
        motifScore = score(motifs)
        if motifScore < bestMotifScore:
            bestMotifs = motifs
            bestMotifScore = motifScore

        count = count + 1
    return bestMotifs
            

    
"""
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\Gibbs Sampling for IRC////////////////////////////
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

"""

"""
The nucleotideFrequencies() function takes in a list of sequences
and returns a dictionary of the frequencies of each of the nucleotides.
"""
def nucleotideFrequencies(sequences):
    c = collections.Counter()
    for seq in sequences:
        for index in range(0, len(seq)):
            c.update(seq[index])
    freqsdict = dict(c)
    totalnucs = 0
    for key in freqsdict:
        totalnucs+=freqsdict.get(key)
        
    for key in freqsdict:
        freqsdict[key]/=totalnucs
      
    return freqsdict
"""
should accept a list of sequences and an
integer k representing the motif size. The function should return a list of size len(sequences) of
integers representing and random start index for a k-mer from each sequence.
"""
def randomStart(sequences, k):
    intList = []
    for index in range(len(sequences)):
        ranNum = rand.randint(0,len(sequences[index])-(k+1))
        intList.append(ranNum)
    return intList
"""
The getMotif() function should accept a list of sequences, a
list of integer start locations, and an integer k representing the motif size. 
The function should return a list of k-mers. Each k-mer should start at the given start 
location and be k characters long
"""    
def getMotif(sequences,startLocations,k):
    kmerList = []
    kmer = ''
    count = 0
    kCount = 0
    for index in range(0,len(sequences)):
        sequence = sequences[index]
        count = 0
        kCount = 0
        kmer = ''
        for ch in range(len(sequence)):
            if startLocations[index] == -1:
                kmerList.append('')
            if startLocations[index] == count and kCount <= k - 1:
                kmer += sequence[ch]
                kCount = kCount + 1
                #print(kmer)
                
            else: 
                count = count + 1
                
        
        kmerList.append(kmer)
        #print(kmerList)    
    return kmerList
                 
"""
The constructProfile() function should accept a list of motifs and should
return a list of dictionaries representing the profile of the k-mers.
If a particular motif is the empty string then it should be ignored in the
 calculation of the profile.

"""           
def constructProfile(motifs):
    profileList = []
    

    for index in range(len(motifs[0])):
        count = {}
        count['A'] = 0
        count['C'] = 0
        count['G'] = 0
        count['T'] = 0
        for ch in motifs:
            count[ch[index]] = count[ch[index]] + 1
        #################### Incrememnting the count by 1
        count['A'] = count['A'] + 1
        count['C'] = count['C'] + 1
        count['G'] = count['G'] + 1
        count['T'] = count['T'] + 1
        #####################
        count['A'] = count['A']/(len(motifs) + 4)
        count['C'] = count['C']/(len(motifs) + 4)
        count['G'] = count['G']/(len(motifs) + 4)
        count['T'] = count['T']/(len(motifs) + 4)
        profileList.append(count)
        
    return profileList

"""
Should accept a profile (a list of dictionaries as returned by 
constructProfile()) and a single string.

profile - List of dictionaries containing the profile matrices of a sequence
kmer - A string representation of the sequence in which the profile matrix is
        constructed from.
"""
def getSingleScore(profile,kmer):
    
    score=1
    for index in range(0,len(kmer)):
        temp = profile[index].get(kmer[index])
        
        score*=temp
    return score
    


"""
The applyProfile() function should accept a profile (a list of
dictionaries as returned by constructProfile()) and a single sequence of any length. 
The profile should be applied to all len(profile) subsequences in sequence and should 
returns a list of numbers of the scores of the profile applied to each of the subsequences

"""
def applyProfile(profile,sequence):
    winSize=len(profile)
    retScores=[] #this is the list of scores that get returned
    for index in range(0,len(sequence)-winSize+1):
        retScores.append(getSingleScore(profile,sequence[index:index+winSize]))
    return retScores
    

"""
– The randomlySelect() function should accept a list of numbers as
input. The function should normalize the numbers (divide by the total so they sum to 1) 
and then randomly (weighted) select and return the index of the selected number.

"""
def randomlySelect(probabilities):
    total = 0
    total=sum(probabilities)
    probabilities=[x/total for x in probabilities]
    chosenNumber = rand.random()
    for index in range(0,len(probabilities)):
        chosenNumber-=probabilities[index]
        if chosenNumber < 0:
            return index
        
    return len(probabilities)-1

"""
The score() function should accept a profile (a list of dictionaries as
returned by constructProfile()) and a dictionary of nucleotide frequencies (as returned by
nucleotideFrequencies) and return a number representing the relative entropy of the profile

"""  
def scoreProfile(profile,nucFreq):
    
    totalDifference = 0    
    
    for dictPos in profile:
        entropy = 0
        freqEntropy = 0
        
        for key, value in dictPos.items():
            entropy+=(value*math.log(value,2))
            freqEntropy+=(value*math.log(nucFreq[key],2))
        totalDifference+=entropy-freqEntropy
    return (totalDifference/len(profile))
"""
 The function should return the best motifs which is the highest
scoring (rather than least as shown in the text) motifs using the relative entropy

sequences - List of DNA sequences
k - the size of the motif being looked for
iterations - number of iterations to run

"""
def gibbsSampling(sequences,k,iterations):
    bestMotifs = []
    i=0
    
    nucFreqs = nucleotideFrequencies(sequences)
    while (i < iterations):
        
        startLoc = randomStart(sequences,k)
        motifList = getMotif(sequences, startLoc, k)
        bestMotifs=list(motifList)
        j=0
        while (j<iterations):
            startLoc = randomStart(sequences,k)
            motifList = getMotif(sequences, startLoc, k)
            
            randomIndex=rand.randint(0,len(motifList)-1)
            tempList=motifList[:randomIndex]
            tempList.extend(motifList[randomIndex + 1:])
            motifProfile = constructProfile(tempList)
            
            appliedProbabilities = applyProfile(motifProfile,sequences[randomIndex])
            newRandIndex = randomlySelect(appliedProbabilities)
            motifList[randomIndex]= getMotif([sequences[randomIndex]], [newRandIndex], k)[0]
            
            contestingMotifProfile = constructProfile(motifList)
            if (scoreProfile(motifProfile, nucFreqs)>scoreProfile(contestingMotifProfile, nucFreqs)):
                bestMotifs=motifList
            j+=1
        i+=1
    
    return bestMotifs

"""
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\MEME for IRC//////////////////////////////////////
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

"""
"""
W - size of motifs looked for
Nsites - Number of motifs in the dataset
Passes - Number of iterations


def meme(dataset, w, nsites, passes):  
    counter = 0
    while counter <= passes:
        nucFreqs = nucleotideFrequencies(dataset)
        motifs = []
        for index in range(len(dataset)):
            for i in range(len(dataset[index - w + 1])):
                if i + w > len(dataset[index]):
                    break
                else:
                    tempMotif = dataset[index][i:i+w]
                    tempMotifPosition = i
                    tempMotifProfile = constructProfile(tempMotif)
                    tempMotifScore = scoreProfile(tempMotifProfile, nucFreqs)
                    motifs.append([tempMotifScore, tempMotif, [index, tempMotifPosition]])
        #sort motifs so highest score is at the beginning of the array
        sortedMotifs = sorted(motifs, key=lambda motif: motif[0])
	length = sortedMotifs.length()
		for index in range(len(sortedMotifs):
			if index = length - 3 || length - 2 || length - 1 || length:
				sortedMotifs.remove(index)
        print(sortedMotifs)
        
        
        #remove nsite motifs from dataset and repeat
        counter += 1
        
    return motifs
"""
def userInputMain():

    funcCall = input("What algorithm would you like to use? Random, Gibbs, MEME ")
    funcCall.lower()
    if funcCall == "random":
        k_size = input("Please enter a k-mer size: ")
        start_time = time.time()
        print(randomizedMotifSearch(fileData,int(k_size)))
        print("--- %s seconds ---" % (time.time() - start_time))
    if funcCall == "gibbs":
        k_size = input("Please enter a k-mer size: ")
        start_time = time.time()
        iterations = input("Please enter the amount of iterations: ")
        print(gibbsSampling(fileData,int(k_size),int(iterations)))
        print("--- %s seconds ---" % (time.time() - start_time))
    if funcCall == "meme":
        return
        
   
fileName = input("Please enter a file name: ")
fileData = readInput(fileName)
userInputMain()