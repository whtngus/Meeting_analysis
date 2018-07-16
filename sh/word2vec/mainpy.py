# -*- coding: utf-8 -*-

import Word2Vec


#load = ["6CM00079.txt","6CM00080.txt","6CM00082.txt","6CM00083.txt","6CM00088.txt","6CM00090.txt","6CM00092.txt","6CM00093.txt","6CM00094.txt","6CM00095.txt"]
load = ["6CM00080.txt"]

# 호출 및 벡터 사이즈 설정 
vector_size = 10
#word2vec = Word2Vec.Word2Vec(pos,vector_size)
word2vec = Word2Vec.Word2Vec(vector_size,load)
final_embeddings, datas, count, dictionary, reverse_dictionary = word2vec.output()
# 유사한 단어 불러오기 
#print(dictionary)
result = word2vec.similarity("군대",100)
print(result)

# 1. 키워드 입력시 유사단어 뽑기
# 2. 주요키워드에서 보여주기 