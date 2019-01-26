import h5py

from keras.models import Sequential
from keras.layers.core import Dense

from dlgo.agent.predict import DeepLearningAgent
from dlgo.data.parallel_processor import GoDataProcessor
from dlgo.encoders.sevenplane import SevenPlaneEncoder
from dlgo.encoders.simple import SimpleEncoder
from dlgo.networks.large import layers
from keras.callbacks import ModelCheckpoint, TensorBoard

go_board_rows, go_board_cols = 19, 19
nb_classes = go_board_rows * go_board_cols
epochs = 250
num_game = 3000
batch_size = 128

encoder = SevenPlaneEncoder((go_board_rows, go_board_cols))
processor = GoDataProcessor(encoder=encoder.name())

input_channels = encoder.num_planes
input_shape = (input_channels, go_board_rows, go_board_cols)

generator = processor.load_go_data('train', num_game, use_generator=True)
test_generator = processor.load_go_data('test', int(num_game / 10), use_generator=True)

model = Sequential()
network_layers = layers(input_shape)
for layer in network_layers:
    model.add(layer)
model.add(Dense(nb_classes, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

model.fit_generator(generator=generator.generate(batch_size, nb_classes),
                    epochs=epochs,
                    steps_per_epoch=generator.get_num_samples() / batch_size,
                    validation_data=test_generator.generate(batch_size, nb_classes),
                    validation_steps=test_generator.get_num_samples() / batch_size,
                    callbacks=[
                        ModelCheckpoint('./checkpoints/large_model_epoch_{epoch}.h5'),
                        TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=128, write_graph=True,
                                    write_grads=True, write_images=True, embeddings_freq=0,
                                    embeddings_layer_names=None, embeddings_metadata=None, embeddings_data=None,
                                    update_freq='batch')]
                    )

model.evaluate_generator(generator=test_generator.generate(batch_size, nb_classes),
                         steps=test_generator.get_num_samples() / batch_size)

# weight_file = './agents/weights.hd5'
# model.save_weights(weight_file, overwrite=True)
# model_file = './agents/model.yml'
# with open(model_file, 'w') as yml:
#     model_yaml = model.to_yaml()
#     yml.write(model_yaml)

deep_learning_bot = DeepLearningAgent(model, encoder)
deep_learning_bot.serialize(h5py.File("./agents/deep_bot.h5"))
