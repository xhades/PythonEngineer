#! /usr/bin/python
# -*-coding: utf-8-*-

from keras.datasets import mnist


import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import matplotlib.pyplot as plt


# 内置load_data() 多次加载数据都是失败 于是下载数据后 自定义方法
def load_data(path="MNIST_data/mnist.npz"):
    f = np.load(path)
    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']
    f.close()
    return (x_train, y_train), (x_test, y_test)

# 训练模型 Start
# 构建序贯模型
def train():
    model = Sequential()
    model.add(Dense(500,input_shape=(784,)))  # 输入层， 28*28=784
    model.add(Activation('tanh'))
    model.add(Dropout(0.3))   # 30% dropout
    model.add(Dense(300))  # 隐藏层， 300
    model.add(Activation('tanh'))
    model.add(Dropout(0.3))   # 30% dropout
    model.add(Dense(10))
    model.add(Activation('softmax'))

    # 编译模型
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)   # 随机梯度下降SGD  ？momentum 暂未理解什么意思 =。=
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return model


def run():
    (x_train, y_train), (x_test, y_test) = load_data()
    X_train = x_train.reshape(x_train.shape[0], x_train.shape[1] * x_train.shape[2])
    X_test = x_test.reshape(x_test.shape[0], x_test.shape[1] * x_test.shape[2])

    Y_train = (np.arange(10) == y_train[:, None]).astype(int)
    Y_test = (np.arange(10) == y_test[:, None]).astype(int)

    model = train()
    model.fit(X_train, Y_train, batch_size=200, epochs=1000, shuffle=True, verbose=1, validation_split=0.3)
    print("Start Test.....\n")
    scores = model.evaluate(X_test, Y_test, batch_size=200, verbose=1)
    print("The Test Loss: %f" % scores[0])



if __name__ == "__main__":
    run()
    # load_data()
    # mnist.load_data()