from h5py import File
from keras import Sequential
from keras.layers import Dense, Activation

from dlgo.agent.pg import PolicyAgent
from dlgo.encoders.simple import SimpleEncoder
from dlgo.networks import large

board_size = 9

encoder = SimpleEncoder((board_size, board_size))
model = Sequential()

for layer in large.layers(encoder.shape()):
    model.add(layer)
model.add(Dense(encoder.num_points()))
model.add(Activation('softmax'))

new_agent = PolicyAgent(model, encoder)

with File('./agents/learning_9x9_base.h5', 'w') as outf:
    new_agent.serialize(outf)
