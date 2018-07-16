# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 19:14:18 2018

@author: Suhyun
"""
import operator
from konlpy.tag import Twitter
import math

class Tf_Ids:
    def __init__(self,doc_size,load_list):
        #데이터 로드
        talk_list = []
        speak_list = []
        
        #load는 리스트 형태  , 한번에 여러문서도가능하도록 --> 나중에는 db형식으로 교체 필요
        for i in load_list:
            #speak는 화자별 이나 사용할 필요가없어보여 일단 내버려둠 
            speak,talk_all = self.load_file(i)
            speak_list.append(speak)
            talk_list = talk_list + talk_all

        # 포스테깅 및 stopword 처리 
        word_list = self.postaging(talk_list)
        
        # tokenization
        words = self.words_join(word_list)
        del word_list
    
    
        self.tf_ids = self.tf_ids(doc_size,words)
        sorted_x = sorted(self.tf_ids.items(), key=operator.itemgetter(1))
        print("tf_ids : ",sorted_x)
        
    
    def tf_ids(self,doc_size,word_list):
        tfds = {} # 구조 단어:[tf,ids,index]
        for i,word in enumerate(word_list):
            if word in tfds:
                #이전 index와 비교하여 doc_size 안에있는경우 tf만 추가
                if tfds[word][2] + doc_size >= i:
                    # doc_size 안에서 추가시 tf만 추가
                    tfds[word][0]+=1
                else:
                    #doc_size를 벗어난 경우 모두 변경 및 index는 초기화
                    tfds[word][0]+=1
                    tfds[word][1]+=1
                    tfds[word][2]+=i
            else:
                #단어가 없는경우 새로 등록
                tfds[word] = [1,1,i]
        #총 문서 갯수 구하기
        doc_count = int(len(word_list) /  doc_size)
        #이제 각 딕셔너리 곱해서 tf_ids로 변경
        tf_ids = {}
        
        #print("tfds : ",tfds)
        
        #http://dev.youngkyu.kr/25 사이트를 참고한 공
        for key,value in tfds.items():
            tf_ids[key] = value[0]* math.log10(doc_count/ value[1])
            
        return tf_ids
        
        
    def words_join(self,words):
        return " ".join(words).split(' ')
    
    
     # 데이터 에서 대화만 가져오기 
    def load_file(self,filesrc):
        f = open(filesrc, 'rt', encoding='utf-16')
        name = ""
        speak = {}
        not_person = ['al', 'ot']
        talk_all = []
        while(True):
            data = f.readline() 
            if not data: break
    
            if("<u who=" in data or "<s n=" in data):
                # 발화자 구분
                if "who" in data:
                    name = data[8:10]
                    if name in not_person:
                        continue
                    if not (name in speak):
                       speak[name] = [] 
    
                # 대화 추출
                temp = data.split(">")
                s = ""
                for v in temp:
                    idx = v.find('<')
                    if idx < 2: continue
                    speak[name].append(v[:idx])
                    talk_all.append(v[:idx])
    
        return speak,talk_all    
       
        
    def postaging(self,docs):
        twitter=Twitter()
        want = ['Exclamation','Adverb','Noun','Alpha','Verb','Adjective']
        want = ['Noun']
        stopword = ['어어','넷','만','것','타','최','태','개','홈','선','끼','각','번','하다','음','화', '이다',' ','다','더','포','제','저','여기','고','씬','첨','난','면','으루','네']
        pos = []
        for i in docs:
            strs = ''
            for t in twitter.pos(i, norm=True, stem=True):
                #if (t[1] in want) and (t[0] not in stopword):
                if (t[1] in want) and (t[0] not in stopword) and (len(t[0]) > 3):
                    strs = strs + " " + t[0]  
        
            pos.append(strs[1:])
        return pos     