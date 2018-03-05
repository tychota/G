import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, ZeroPadding2D, Activation

# from keras import backend as K
# K.set_image_dim_ordering('tf')
from keras.optimizers import Adadelta

np.random.seed(1234)

X = np.load("./data/features_9x9_7p.npy")
Y = np.load("./data/labels_9x9_7p.npy")

samples = X.shape[0]
size = 9
input_shape = (size, size, 7)

X = X.reshape(samples, *input_shape)
print(len(X))
print(len(Y))

train_samples = 400
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

model = Sequential()
model.add(ZeroPadding2D((3, 3), input_shape=input_shape, data_format='channels_first'))
model.add(Conv2D(64, (7, 7), padding='valid', data_format='channels_first'))
model.add(Activation('relu'))

model.add(ZeroPadding2D((2, 2), data_format='channels_first'))
model.add(Conv2D(64, (5, 5), data_format='channels_first'))
model.add(Activation('relu'))

model.add(ZeroPadding2D((2, 2), data_format='channels_first'))
model.add(Conv2D(64, (5, 5), data_format='channels_first'))
model.add(Activation('relu'))

model.add(ZeroPadding2D((2, 2), data_format='channels_first'))
model.add(Conv2D(48, (5, 5), data_format='channels_first'))
model.add(Activation('relu'))

model.add(ZeroPadding2D((2, 2), data_format='channels_first'))
model.add(Conv2D(48, (5, 5), data_format='channels_first'))
model.add(Activation('relu'))

model.add(ZeroPadding2D((2, 2), data_format='channels_first'))
model.add(Conv2D(32, (5, 5), data_format='channels_first'))
model.add(Activation('relu'))

model.add(ZeroPadding2D((2, 2), data_format='channels_first'))
model.add(Conv2D(32, (5, 5), data_format='channels_first'))
model.add(Activation('relu'))

model.add(Flatten())
model.add(Dense(1024))
model.add(Activation('relu'))

model.add(Dense(size * size))
model.add(Activation('softmax'))

opt = Adadelta(clipnorm=0.25)

model.summary()
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

model.fit(X_train, Y_train, batch_size=64, epochs=5, verbose=1, validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])
