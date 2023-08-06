# Importing the necessary librarires to the below class

import pandas as pd
import numpy as np
import nltk
import string

nltk.download('stopwords')
from nltk.corpus import stopwords

from nltk.stem import SnowballStemmer
snowball = SnowballStemmer('english')

np.array(stopwords.words('english')) # List of stopwords

class shourya_306:
  
    def __init__(self,row):
        self.row = row

    def removing_punc(self):
        no_punc_list = []
        '''This function is used to remove punctations from the data'''
        for letter in self.row:
            if letter not in string.punctuation:
                no_punc_list.append(letter)
        return ''.join(no_punc_list)
    
    def removing_stopwords(self):
        no_stopwords_list = []
        '''This function returns the text column without the stopwords'''
        split_text = self.row.split()
        for word in split_text:
            if word not in stopwords.words('english'):
                no_stopwords_list.append(word)
        no_stopwords =  ' '.join(no_stopwords_list)
        return no_stopwords
    
    def standard(self):

        stem_list = []
        '''This function performs stemming'''
        split_row = self.row.split()
        for word in split_row:
            stem_list.append(snowball.stem(word))
        return ' '.join(stem_list)
    
