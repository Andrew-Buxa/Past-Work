# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 22:37:04 2017

This program takes in a file of generated hexidecimal digests of a password and the actual
password itself. Then, the program converts them into binary and either writes the converted data
to a training data file or test data file at random.

@author: Andrew Buxa
"""
maxChars = 8  
maxLength = 128 
dataFiles = 2
count = 1


# While loop which generates passwords and digests into binary and then based on what count is, either
# fills up the training data with binary conversions or the test data with binary conversions.
while (count <= 2):
    if (count == 1):
        file = open("trainingData.txt","r")
        newFile = open("trainDataConv.txt","w")
    else:
        file = open("testData.txt","r")
        newFile = open("testDataConv.txt","w")

    # Iterates over the input file, splitting and converting the data acquired
    # into binary.
    for line in file:
        snippet = line.split(' ')    
        theSnippet = bin(int(snippet[0],16))[2:]
        unhashPass = snippet[1].rstrip('\n')
        unhashBin = ""
        clearedHashBin = ""
        hexLetter = ""
        hexDigest = ""
        hexDigest += theSnippet
        index = 0
        # Turns each character in the generated password into it's hex form, then
        # convert the hex number into binary. Then, append it onto a blank string.
        
        for letter in range(len(unhashPass)):
            hexLetter = hex(ord(unhashPass[letter]))
            hexLetter = int(hexLetter, 16)
            unhashBin = bin(hexLetter)
            unhashBin= unhashBin.replace("0b","")
            length = len(unhashBin)
            difference = maxChars - length
            unhashBin = ("0" * difference) + unhashBin
            clearedHashBin += unhashBin
            
        
        # If the binary form of the hexdigest is smaller than 128 bits, which is due
        # to the conversion into a number (cutting off leading 0's), then add 0's up 
        # until the length is 128.
        if (str(len(theSnippet)) < "128"):   
            zeroNeeded = maxLength - int(len(theSnippet))
            zeroAdded = ""
            index = 0
            while index < zeroNeeded:
                zeroAdded += "0"
                index = index + 1
            theSnippet = zeroAdded + theSnippet
        newFile.write(theSnippet+" "+clearedHashBin+'\n')
    newFile.close()
    count+=1