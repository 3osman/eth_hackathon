from scipy.stats import multivariate_normal
import numpy as np
import math
# Load the training text
f_training_text = open('count_2l.txt', 'r')
training_text = f_training_text.read()
f_training_text.close()

# Initalize a structure to count character-to-character transitions, include a start-of-word one-way transition denoted '_'
transition_counts = np.matlib.zeros((28,27))
from_ids = {'_':0,'a':1,'b':2,'c':3,'d':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11, 'l':12, 'm':13, 'n':14, 'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21, 'v':22, 'w':23, 'x':24, 'y':25,'z':26, 'space':27}
to_ids = {'a':0,'b':1,'c':2,'d':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13, 'o':14, 'p':15, 'q':16, 'r':17, 's':18, 't':19, 'u':20, 'v':21, 'w':22, 'x':23, 'y':24,'z':25, 'space':26}

# Split the training text into words
training_words = training_text.split('\n')

# Count character transitions
for line in training_words:
    prev_character = line[0]
    character = line[1]
    count = line.split('\t')[1]
    #print(prev_character)
    #print(character)
    #print(count)
    #for character in word:
        # TODO: Update the transition_counts matrix, make use of from_ids and to_ids
    transition_counts[from_ids[prev_character],to_ids[character]] = count
        # Update previous character
    #prev_character = character

# TODO: Apply smoothing (if necessary) and convert the transition counts into a useful bigram
i = 0
for row in transition_counts:
    if row.sum() != 0:
    	#print row.sum()
        transition_counts[i] = row / row.sum() 
        #print row.sum()

    i += 1
print transition_counts