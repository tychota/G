import h5py

from keras.models import Sequential
from keras.layers.core import Dense

from dlgo.agent.predict import DeepLearningAgent
from dlgo.data.parallel_processor import GoDataProcessor
from dlgo.encoders.sevenplane import SevenPlaneEncoder
from dlgo.networks.large import layers
from keras.callbacks import ModelCheckpoint, TensorBoard

from kerasutils import set_gpu_memory_target

go_board_rows, go_board_cols = 19, 19
nb_classes = go_board_rows * go_board_cols
epochs = 20
num_game = 7000
batch_size = 64

encoder = SevenPlaneEncoder((go_board_rows, go_board_cols))
processor = GoDataProcessor(encoder=encoder.name())

input_channels = encoder.num_planes
input_shape = (input_channels, go_board_rows, go_board_cols)

X, y = processor.load_go_data('train', num_game)
X_test, y_test = processor.load_go_data('test', int(num_game / 10))

model = Sequential()
network_layers = layers(input_shape)
for layer in network_layers:
    model.add(layer)
model.add(Dense(nb_classes, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

filepath = "./checkpoints/large_model_best.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
tensorboard = TensorBoard(log_dir='./logs', histogram_freq=1, batch_size=batch_size, write_graph=True,
                          write_grads=True, write_images=True, embeddings_freq=0,
                          update_freq='epoch')
callbacks_list = [checkpoint, tensorboard]

import tensorflow as tf

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    set_gpu_memory_target(0.7)
    model.fit(x=X, y=y, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test),
              callbacks=callbacks_list)
    evaluation = model.evaluate(x=X_test, y=y_test, batch_size=batch_size)
    print(evaluation)

deep_learning_bot = DeepLearningAgent(model, encoder)
deep_learning_bot.serialize(h5py.File("./agents/deep_bot_2.h5"))
