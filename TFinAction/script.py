# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
@author: xhades
@Date: 2017/12/29

"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
# 查看一下训练集
print(mnist.train.images.shape, mnist.train.labels.shape)
# 查看一下验证集合
print(mnist.validation.images.shape, mnist.validation.labels.shape)


# train
sess = tf.InteractiveSession()
x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x, W)+ b)
y_ =tf.placeholder(tf.float32, [None, 10])
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)


tf.global_variables_initializer().run()

for i in range(10):
    print("-->", i)
    batch_xs, batch_ys = mnist.train.next_batch(100)
    train_step.run(feed_dict={x: batch_xs, y_:batch_ys})

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
print("==>", correct_prediction)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(accuracy.eval({x: mnist.test.images, y_: mnist.test.labels}))






