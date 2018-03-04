import numpy as np
from keras.models import Sequential
from keras.layers import Dense

np.random.seed(1234)

X = np.load("./data/features.npy")
Y = np.load("./data/labels.npy")

samples = X.shape[0]
board_size = 5 * 5

X = X.reshape(samples, board_size)
Y = Y.reshape(samples, board_size)
print(len(X))
train_samples = 200
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

model = Sequential()
model.add(Dense(200, activation='sigmoid', input_shape=(board_size,)))
model.add(Dense(300, activation='sigmoid'))
model.add(Dense(200, activation='sigmoid'))
model.add(Dense(board_size, activation='sigmoid'))
model.summary()
model.compile(loss='mean_squared_error',
    optimizer='sgd',
    metrics=['accuracy'])
model.fit(X_train, Y_train,
    batch_size=64,
    epochs=5,
    verbose=1,
    validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
