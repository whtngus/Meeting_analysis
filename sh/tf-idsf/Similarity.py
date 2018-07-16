# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 22:29:14 2018

@author: Suhyun
"""


# -*- coding: utf-8 -*-

import random
import numpy as np
import tensorflow as tf
import collections
import math
from six.moves import xrange
from konlpy.tag import Twitter
from six.moves import xrange


class Similarity:
    def __init__(self,load_path,load_name):
        #데이터 로드
        '''
        로드 작업 ... 2가지 변수와 유사도 비교할걸 뽑아옴 
        self.final_embeddings  = get~~
        self.dictionary = get ~~
        
        '''
        
     


    def similarity(self,find_word,top_word):
        find_word_data = self.final_embeddings[self.dictionary[find_word]]
        sims = []
        for key,value in  self.dictionary.items():
            similarity = self.final_embeddings[value]
            cosine_similarity = np.dot(find_word_data, similarity)/(np.linalg.norm(find_word_data)* np.linalg.norm(similarity))
            sims.append([cosine_similarity,key])
        sims.sort(reverse=True)
        return sims[1:top_word+1]
    