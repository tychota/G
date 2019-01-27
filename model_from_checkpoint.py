import h5py

from keras.layers import Dense

from dlgo.agent.predict import DeepLearningAgent
from dlgo.encoders.sevenplane import SevenPlaneEncoder
from dlgo.networks.large import layers
from keras import Sequential

go_board_rows, go_board_cols = 19, 19
nb_classes = go_board_rows * go_board_cols
epochs = 250
num_game = 3000
batch_size = 128

encoder = SevenPlaneEncoder((go_board_rows, go_board_cols))

input_channels = encoder.num_planes
input_shape = (input_channels, go_board_rows, go_board_cols)

model = Sequential()
network_layers = layers(input_shape)
for layer in network_layers:
    model.add(layer)
model.add(Dense(nb_classes, activation='softmax'))
model.summary()
model.load_weights("./checkpoints/large_model_best.h5")

model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

deep_learning_bot = DeepLearningAgent(model, encoder)
deep_learning_bot.serialize(h5py.File("./agents/deep_bot.h5"))
