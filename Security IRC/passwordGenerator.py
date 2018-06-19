# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 18:25:51 2017

This program uses the string of possible password characters and generates all permutations
of the password, given a certain length for the password. 

Note: The larger the password size, the amount of permutations grows EXPONENTIALLY.

@author: Andrew Buxa
"""
import hashlib
from itertools import permutations
from random import randint
possibleChars = "!#$%&'()*+,-.0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
m = hashlib.md5()
file = open("trainingData.txt","w")
fileTwo = open("testData.txt","w")
# For loop which generates EVERY possible permutation for passwords of length x
# (length is the second paramter in the permutations method)
for p in permutations(possibleChars,3):
    charPass = ""
    ranNum = randint(0,6000)
    for index in p:
        charPass += index
    pasw = charPass.encode('utf-8') # encoding the data before converting it in MD5
    m.update(pasw) # updating the hashlib with the encoded data
    if (ranNum >= 5750):
        fileTwo.write(m.hexdigest()+" "+charPass+'\n')
    else:
        file.write(m.hexdigest()+" "+charPass+'\n')
file.close()
fileTwo.close()
