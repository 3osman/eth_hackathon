from scipy.stats import multivariate_normal
import numpy as np
import math
# Load the training text
f_training_text = open('big.txt', 'r')
training_text = f_training_text.read()
f_training_text.close()

# Initalize a structure to count character-to-character transitions, include a start-of-word one-way transition denoted '_'
counts = np.zeros(26)
chars = {'a':0,'b':1,'c':2,'d':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13, 'o':14, 'p':15, 'q':16, 'r':17, 's':18, 't':19, 'u':20, 'v':21, 'w':22, 'x':23, 'y':24,'z':25}

# Split the training text into words
training_words = training_text.split('\n')

# Count character transitions
for line in training_words:
    words = line.split(' ')
    for word in words:

        for char in word:

            #print len(counts)
            #print(char)
            if char.lower() in chars.keys():
                #if char.lower()=='z':
                    #print("ZZZZZZZZZZz")
                    #print(counts[chars[char.lower()]]) 

                #print(char.lower())
                counts[chars[char.lower()]] += 1
    #print(prev_character)
    #print(character)
    #print(count)
    #for character in word:
        # TODO: Update the transition_counts matrix, make use of from_ids and to_ids
        # Update previous character
    #prev_character = character

# TODO: Apply smoothing (if necessary) and convert the transition counts into a useful bigram
counts /= counts.sum() 
print counts