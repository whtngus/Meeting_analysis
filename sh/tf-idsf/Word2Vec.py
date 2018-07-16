# -*- coding: utf-8 -*-

import random
import numpy as np
import tensorflow as tf
import collections
import math
from six.moves import xrange
from konlpy.tag import Twitter
from six.moves import xrange


class Word2Vec:
    # 데이터 에서 대화만 가져오기 
    def load_file(self,filesrc):
        f = open(filesrc, 'rt', encoding='utf-16')
        name = ""
        talk = []
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

    def words_join(self,words):
        return " ".join(words).split(' ')
    
    def postaging(self,docs):
        twitter=Twitter()
        want = ['Exclamation','Adverb','Noun','Alpha','Verb','Adjective']
        stopword = ['어어','넷','만','것','타','최','태','개','홈','선','끼','각','번','하다','음','화', '이다',' ','다','더','포','제','저','여기','고','씬','첨','난','면','으루','네']
        pos = []
        for i in docs:
            strs = ''
            for t in twitter.pos(i, norm=True, stem=True):
                if (t[1] in want) and (t[0] not in stopword):
                    strs = strs + " " + t[0]  
        
            pos.append(strs[1:])
        return pos
    
    # word_list를 불러오기전 함수 
    #def __init__(self, word_list,vector_size,load_list):
    
    def __init__(self,vector_size,load_list):
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
    
        #테스트 데이터로 확인식 보통 단어수 2000개를 넘지 못함 
        self.vocabulary_size = 4000# 원핫 인코딩 시킬 단어의 갯수   
        words = self.words_join(word_list)
        print("len(words) : ",len(words))
        self.data, self.count, self.dictionary, self.reverse_dictionary = self.build_dataset(words)
        del words
        self.batch, self.labels = self.generate_batch(batch_size=8, num_skips=2, skip_window=1)
        self.batch_size = 32
        self.embedding_size = vector_size  # embedding vector의 크기. 아웃풋 크기 
        self.skip_window = 3       # 윈도우 크기 : 왼쪽과 오른쪽으로 얼마나 많은 단어를 고려할지를 결정.
        self.num_skips = 2         # 레이블(label)을 생성하기 위해 인풋을 얼마나 많이 재사용 할 것인지를 결정.
        
        # sample에 대한 validation set은 원래 랜덤하게 선택해야한다. 하지만 여기서는 validation samples을 
        # 가장 자주 생성되고 낮은 숫자의 ID를 가진 단어로 제한한다.
        #self.valid_size = 16     # validation 사이즈.
        #self.valid_window = 3  # 분포의 앞부분(head of the distribution)에서만 validation sample을 선택한다.
        #self.valid_examples = np.random.choice(self.valid_window, self.valid_size, replace=False)
        #self.valid_examples = np.random.choice(self.valid_window, self.valid_size, replace=True)        
        self.num_sampled = 64    # sample에 대한 negative examples의 개수.
        self.num_steps = 30001  # server 시 올리
        
        self.final_embeddings = self.train(self.reverse_dictionary,self.data)
        
        
    def output(self):
        return self.final_embeddings, self.data, self.count, self.dictionary, self.reverse_dictionary
      
        
    def train(self,reverse_dictionary,data):
        graph = tf.Graph()
        with graph.as_default():
        
          # 트레이닝을 위한 인풋 데이터들
          train_inputs = tf.placeholder(tf.int32, shape=[self.batch_size])
          train_labels = tf.placeholder(tf.int32, shape=[self.batch_size, 1])
        
          # Ops and variables pinned to the CPU because of missing GPU implementation
          with tf.device('/cpu:0'):
            # embedding vectors 행렬을 랜덤값으로 초기화
              embeddings = tf.Variable(
                    tf.random_uniform([self.vocabulary_size, self.embedding_size], -1.0, 1.0))
            # 행렬에 트레이닝 데이터를 지정
              embed = tf.nn.embedding_lookup(embeddings, train_inputs)
        
              # NCE loss를 위한 변수들을 선언
              nce_weights = tf.Variable(tf.truncated_normal([self.vocabulary_size, self.embedding_size], stddev=1.0 / math.sqrt(self.embedding_size)))
              nce_biases = tf.Variable(tf.zeros([self.vocabulary_size]))
        
          # batch의 average NCE loss를 계산한다.
          # tf.nce_loss 함수는 loss를 평가(evaluate)할 때마다 negative labels을 가진 새로운 샘플을 자동적으로 생성한다.
          loss = tf.reduce_mean(
              tf.nn.nce_loss(weights=nce_weights,
                             biases=nce_biases,
                             labels=train_labels,
                             inputs=embed,
                             num_sampled=self.num_sampled,
                             num_classes=self.vocabulary_size))
        
          optimizer = tf.train.AdamOptimizer(0.01).minimize(loss)
        
        
          # minibatch examples과 모든 embeddings에 대해 cosine similarity를 계산한다.
          norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
          normalized_embeddings = embeddings / norm

        with tf.Session(graph=graph) as session:
          # 트레이닝을 시작하기 전에 모든 변수들을 초기화한다.
            tf.initialize_all_variables().run()
            print("Initialized")
        
            average_loss = 0
            for step in xrange(self.num_steps):
                batch_inputs, batch_labels = self.generate_batch(self.batch_size, self.num_skips, self.skip_window)
                feed_dict = {train_inputs : batch_inputs, train_labels : batch_labels}
            
            # optimizer op을 평가(evaluating)하면서 한 스텝 업데이트를 진행한다.
                _, loss_val = session.run([optimizer, loss], feed_dict=feed_dict)
                average_loss += loss_val
        
                if step % 2000 == 0:
                    if step > 0:
                        average_loss /= 2000
                    # 평균 손실(average loss)은 지난 2000 배치의 손실(loss)로부터 측정된다.
                    print("Average loss at step ", step, ": ", average_loss)
                    average_loss = 0
                
                final_embeddings = normalized_embeddings.eval(session=session)

                
        return final_embeddings
          
    
    def build_dataset(self,words):
      count = [['UNK', -1]]
      count.extend(collections.Counter(words).most_common(self.vocabulary_size - 1))
      dictionary = dict()
      for word, _ in count:
        dictionary[word] = len(dictionary)
      data = list()
      unk_count = 0
      for word in words:
        if word in dictionary:
          index = dictionary[word]
        else:
          index = 0  # dictionary['UNK']
          unk_count += 1
        data.append(index)
      count[0][1] = unk_count
      reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
      return data, count, dictionary, reverse_dictionary
    
    
    # Step 3: skip-gram model을 위한 트레이닝 데이터(batch)를 생성하기 위한 함수.
    def generate_batch(self,batch_size, num_skips, skip_window):
        data_index = 0
        #global data_index
        assert batch_size % num_skips == 0
        assert num_skips <= 2 * skip_window
        batch = np.ndarray(shape=(batch_size), dtype=np.int32)
        labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
        span = 2 * skip_window + 1 # [ skip_window target skip_window ]
        buffer = collections.deque(maxlen=span)
        
        for _ in range(span):
            buffer.append(self.data[data_index])
            data_index = (data_index + 1) % len(self.data)
        for i in range(batch_size // num_skips):
            target = skip_window  # target label at the center of the buffer
            targets_to_avoid = [ skip_window ]
            for j in range(num_skips):
                while target in targets_to_avoid:
                    target = random.randint(0, span - 1)
                targets_to_avoid.append(target)
                batch[i * num_skips + j] = buffer[skip_window]
                labels[i * num_skips + j, 0] = buffer[target]
            buffer.append(self.data[data_index])
            data_index = (data_index + 1) % len(self.data)
        return batch, labels


    def similarity(self,find_word,top_word):
        find_word_data = self.final_embeddings[self.dictionary[find_word]]
        sims = []
        for key,value in  self.dictionary.items():
            similarity = self.final_embeddings[value]
            cosine_similarity = np.dot(find_word_data, similarity)/(np.linalg.norm(find_word_data)* np.linalg.norm(similarity))
            sims.append([cosine_similarity,key])
        sims.sort(reverse=True)
        return sims[1:top_word+1]
    