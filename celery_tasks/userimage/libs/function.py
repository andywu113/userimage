# Create your views here.
from statsmodels.sandbox.stats.diagnostic import acorr_ljungbox
import tensorflow as tf
import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import MinMaxScaler
from .data_transform import trueData
import warnings
warnings.filterwarnings("ignore")

#利用自编码网络进行降维
def AutoEncoder(i,begin,end):
    """
    :param i: 表示第i家企业
    :param begin: 选取数据的起始天数
    :param end:选取数据的结束天数
    :return:降维后的新数据，为一个数组
    """
    dataOrigin = trueData(i,begin,end)
    trans = MinMaxScaler()
    data_trans = trans.fit_transform(dataOrigin)
    learning_rate = 0.07
    n_iterations = 100
    n_hidden_1 = 48
    n_hidden_2 = 24
    n_hidden_3 = 9
    n_input = 96
    X = tf.placeholder(tf.float32, shape=[None, n_input])
    weights = {
        "encoder_h1": tf.Variable(tf.random_normal([n_input, n_hidden_1])),
        "encoder_h2": tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
        "encoder_h3": tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3])),
        "decoder_h1": tf.Variable(tf.random_normal([n_hidden_3, n_hidden_2])),
        "decoder_h2": tf.Variable(tf.random_normal([n_hidden_2, n_hidden_1])),
        "decoder_h3": tf.Variable(tf.random_normal([n_hidden_1, n_input]))
    }
    biases = {
        "encoder_b1": tf.Variable(tf.random_normal([n_hidden_1])),
        "encoder_b2": tf.Variable(tf.random_normal([n_hidden_2])),
        "encoder_b3": tf.Variable(tf.random_normal([n_hidden_3])),
        "decoder_b1": tf.Variable(tf.random_normal([n_hidden_2])),
        "decoder_b2": tf.Variable(tf.random_normal([n_hidden_1])),
        "decoder_b3": tf.Variable(tf.random_normal([n_input]))
    }

    def encoder(x):
        layer_1 = tf.sigmoid(tf.add(tf.matmul(x, weights["encoder_h1"]), biases["encoder_b1"]))
        layer_2 = tf.sigmoid(tf.add(tf.matmul(layer_1, weights["encoder_h2"]), biases["encoder_b2"]))
        layer_3 = tf.add(tf.matmul(layer_2, weights["encoder_h3"]), biases["encoder_b3"])
        return layer_3

    def decoder(x):
        layer_1 = tf.sigmoid(tf.add(tf.matmul(x, weights["decoder_h1"]), biases["decoder_b1"]))
        layer_2 = tf.sigmoid(tf.add(tf.matmul(layer_1, weights["decoder_h2"]), biases["decoder_b2"]))
        output = tf.sigmoid(tf.add(tf.matmul(layer_2, weights["decoder_h3"]), biases["decoder_b3"]))
        return output

    encoder_op = encoder(X)
    decoder_op = decoder(encoder_op)
    y_pred = decoder_op
    y_true = X
    cost = tf.reduce_mean(tf.square(y_pred - y_true))
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)
    init = tf.global_variables_initializer()
    X_train = data_trans
    co = []
    with tf.Session() as sess:
        sess.run(init)
        for iteration in range(n_iterations):
            _, c = sess.run([optimizer, cost], feed_dict={X: X_train})
            co.append(c)
        newFeatureData = sess.run(encoder_op, feed_dict={X: X_train})
        # outputData = sess.run(decoder_op,feed_dict={X:X_train})
                # plt.figure(figsize=(20,4))
                # plt.rcParams['font.sans-serif']=['SimHei']
                # plt.rcParams['axes.unicode_minus']=False
                # plt.plot(list(range(n_iterations)),co)
                # plt.title("损失函数变化曲线")
                # plt.show()
    return newFeatureData


