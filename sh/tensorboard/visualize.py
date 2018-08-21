import sys, os
from gensim.models import Word2Vec
import tensorflow as tf
import numpy as np
from tensorflow.contrib.tensorboard.plugins import projector

#visualize using tensorboard
class Visualize:

    '''
        - mode_path : stored model path
        - output_path : observation path
        - vector_size : Vector size applied during learning
    '''
    def __init__(self,mode_path,output_path):
        #저장된 모델 load
        model = Word2Vec.load(mode_path)
        # tensorboard 저장 형식
        meta_file = "w2x_metadata.tsv"
        placeholder = np.zeros((len(model.wv.index2word), model.vector_size))

        # output_path경로가 없는경우 생성
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        # 이미 생성된 output 이 있는경우 새로만들어야함으로 삭제
        else:
            filelist = [f for f in os.listdir(output_path)]
            for f in filelist:
                try:
                    os.remove(os.path.join(output_path, f))
                except Exception as e:
                    print("엑세스 거부 :",e)


        with open(os.path.join(output_path,meta_file), 'wb') as file_metadata:
            for i, word in enumerate(model.wv.index2word):
                placeholder[i] = model[word]
                # temporary solution for https://github.com/tensorflow/tensorflow/issues/9094
                if word == '':
                    print("Emply Line, should replecaed by any thing else, or will cause a bug of tensorboard")
                    file_metadata.write("{0}".format('<Empty Line>').encode('utf-8') + b'\n')
                else:
                    file_metadata.write("{0}".format(word).encode('utf-8') + b'\n')

        # define the model without training
        sess = tf.InteractiveSession()

        embedding = tf.Variable(placeholder, trainable = False, name = 'w2x_metadata')
        tf.global_variables_initializer().run()

        saver = tf.train.Saver()
        writer = tf.summary.FileWriter(output_path, sess.graph)

        # adding into projector
        config = projector.ProjectorConfig()
        embed = config.embeddings.add()
        embed.tensor_name = 'w2x_metadata'
        embed.metadata_path = meta_file

        # Specify the width and height of a single thumbnail.
        projector.visualize_embeddings(writer, config)
        saver.save(sess, os.path.join(output_path,'w2x_metadata.ckpt'))
        print('Run `tensorboard --logdir={0}` to run visualize result on tensorboard'.format(output_path))
        self.run_str = "tensorboard --logdir={0}".format(output_path)

    def run_tensorboard(self):
        os.system(self.run_str)




if __name__ == '__main__' :
    # 트레이닝된 word2vec 모델명, tensorboard file path
    visualize = Visualize("word2vec.model","./test")
    # 텐서보드 실행
    visualize.run_tensorboard()
