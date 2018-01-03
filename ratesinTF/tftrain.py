# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
@author: xhades
@Date: 2018/1/2

"""
import tensorflow as tf


class RatesTrain(object):
    def __init__(self, nb_input, nb_output, nb_features,hidden_units=1):
        self.nb_input = nb_input
        self.nb_output = nb_output
        self.weigths, self.b1 = self.init_weights()
        self.nb_features = nb_features
        self.hidden_units = hidden_units
        self.W_output = tf.Variable(tf.zeros([self.hidden_units, 2]))
        self.b2 = tf.Variable(tf.zeros([2]))

    def init_weights(self):
        W = tf.get_variable("W", shape=[self.nb_features, self.hidden_units], initializer=tf.contrib.layers.xavier_initializer())
        b1 = tf.Variable(tf.zeros([self.hidden_units]))
        return W, b1

    def build_model(self):
        # init placeholder,weights and dropout rate
        x = tf.placeholder(tf.float32, [None, self.nb_input])
        keep_prob = tf.placeholder(tf.float32)
        hidden = tf.nn.relu(tf.matmul(x, self.weigths) + self.b1)
        hidden_drop = tf.nn.dropout(hidden, keep_prob)

        # softmax
        self.y = tf.nn.softmax(tf.matmul(hidden_drop, self.W_output) + self.b2)
        self.y_ = tf.placeholder(tf.float32, [None, 2])
        # loss
        self.cross_entropy = self.calc_cost()
        # train op
        self.optimizer = tf.train.AdagradOptimizer(0.3).minimize(self.cross_entropy)

        # init all variables
        self.ss = tf.Session()
        self.ss.run(tf.global_variables_initializer())

    def fit(self):

        nb_train = ''
        for i in range(2130):
            batch_xs, barch_ys = ''
            pass



    def calc_cost(self):
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(self.y_ * tf.log(self.y), reduction_indices=[1]))
        return cross_entropy



if __name__ == "__main__":
    nb_input = 128
    nb_output =2
    rt = RatesTrain()