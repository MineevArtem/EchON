from keras.models import load_model, Model
from keras.layers import Conv2DTranspose, Conv2D, Input, MaxPooling2D, Dropout, LeakyReLU
from keras.callbacks import ReduceLROnPlateau, TensorBoard
import os
import script
import time
from load_data import test_data, form_test_data
import numpy as np
import scipy.misc
from shutil import rmtree
from matplotlib import pyplot as plt
from load_data import map_build
import math


class Neural_Network():
    def __init__(self):
        self.answer = 0
        inputs = Input(shape=(32, 32, 4))
        conv_1 = Conv2D(50, (4, 4), activation='relu', padding='same')(inputs)
        max_1 = MaxPooling2D((4, 2), padding='same')(conv_1)
        conv_3 = Conv2D(50, (4, 4), activation='relu', padding='same')(max_1)
        max_3 = MaxPooling2D((2, 2), padding='same')(conv_3)
        hidden = Conv2D(50, (10, 10), activation='relu', padding='same')(max_3)
        drop = Dropout(0.25)(hidden)
        deconv_1 = Conv2DTranspose(50, (4, 4), strides=(4, 4), padding='same', activation='relu')(drop)
        drop1 = Dropout(0.5)(deconv_1)
        deconv_2 = Conv2DTranspose(50, (4, 4), strides=(4, 4), padding='same', activation='relu')(drop1)
        drop2 = Dropout(0.5)(deconv_2)
        deconv_3 = Conv2DTranspose(1, (10, 10), strides=(2, 2), padding='same', activation='relu')(drop2)
        self.model = Model(inputs=[inputs], outputs=[deconv_3])
        self.learned = False
        self.model.compile(optimizer='adam', loss='mse', metrics=['acc'])
        self.model.summary()

    def fit_model(self, data, answers):
        epochs = int(input('Epochs: '))
        self.history = self.model.fit(x=data, y=answers, batch_size=32, epochs=epochs, validation_split=0.3)
        self.learned = True

    def work_neural_network(self, app, zet_path):
        success = False
        data = []
        while not success:
            try:
                script.save_data(app)
                time.sleep(0.5)
                data = test_data(zet_path)
                os.remove(zet_path + '/oscgrph_1.dtu')
                print("Готово!")
                success = True
                rmtree(zet_path)
            except Exception as e:
                try:
                    rmtree(zet_path)
                except:
                    pass
                input(str(e))

        answer = self.model.predict(data)
        print(np.max(answer))
        # answer = answer / np.max(answer)
        answer = answer.reshape(128, 256)
        # for row in answer:
        #    print(' '.join([str(elem) for elem in row]))
#        self.distance(answer)
        self.distance2(answer)
        self.draw(answer)

    def test(self):
        b = int(input())
        c = int(input())
        aa = map_build(b, c)
        aa = aa.reshape(128, 256)
        a = scipy.misc.toimage(aa, cmin=0.0)
        a.show()

    def draw(self, answer):

        b = scipy.misc.toimage(answer, cmin=0.0)
        b = b.resize((answer.shape[1] * 2, answer.shape[0] * 2))
        # b.save('123.bmp')
        b.show()

    def load_neural_network(self):
        if len(os.listdir(os.getcwd() + "/neural_networks/")) == 0:
            input("No saved neural networks")
            return
        print("Select file:\n", os.listdir(os.getcwd() + "/neural_networks/"))
        name = input()
        self.model = load_model(os.getcwd() + "/neural_networks/" + name + ".h5")
        self.model.compile(optimizer='sgd', loss='mse', metrics=['acc'])
        self.learned = True

    def save_neural_network(self):
        name = input("File name: ")
        try:
            os.mkdir(os.getcwd() + '/neural_networks')
        except:
            pass
        self.model.save(os.getcwd() + "/neural_networks/" + name + ".h5")

    def plotting(self):
        # Plot training & validation accuracy values
        plt.plot(self.history.history['acc'])
        plt.plot(self.history.history['val_acc'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.show()

        # Plot training & validation loss values
        plt.plot(self.history.history['loss'])
        plt.plot(self.history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.show()

    def distance(self, answer):
        masses = []
        for row in answer:
            sum = 0
            for elem in row:
                sum = sum + elem
            masses.append(sum)
        mass = 0
        for elem in masses:
            mass = mass + elem
        sum = 0
        i = 0
        for elem in masses:
            sum = sum + elem
            i += 1
            if sum > mass / 2:
                break
        dist = (128 - i) / 128 * 0.5
#        for elem in masses:
#            print(elem, end=" ")
#        print()
        print("Distance:", dist, sep=" ")

    def distance2(self, answer):
        masses = []
        for row in answer:
            sum = 0
            for elem in row:
                sum = sum + elem
            masses.append(sum)
        mass = 0
        i = 1
        for elem in masses:
            mass = mass + elem * i
            i += 1
        sum = 0
        for elem in masses:
            sum = sum + elem
        i = math.floor(mass / sum)
        dist = (128 - i) / 128 * 0.5
#        for elem in masses:
#            print(elem, end=" ")
#        print()
        print("Distance:", dist, sep=" ")
