import tensorflow as tf
import numpy as np
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def nn(filename):
    path = os.getcwd() + "\\apps\\users\\check\\model\\"

    def get_data(filename):

        line_list = []
        with open(filename, 'r', encoding='UTF-8') as f:
            for line in f:
                line_list.append(line.strip().split())
            data = np.array(line_list)

        return data

    x = get_data(filename)

    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(path + 'model.ckpt.meta')
        saver.restore(sess, path + 'model.ckpt')
        pred = tf.get_collection('network-output')[0]

        graph = tf.get_default_graph()
        xs = graph.get_operation_by_name('xs').outputs[0]

        y = sess.run(pred, feed_dict={xs: x})

    return y
