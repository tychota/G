from dlgo.data.parallel_processor import GoDataProcessor
from dlgo.encoders.simple import SimpleEncoder

from dlgo.networks import small
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import Adadelta
from keras.callbacks import ModelCheckpoint, TensorBoard

go_board_rows, go_board_cols = 19, 19
num_classes = go_board_rows * go_board_cols
num_games = 300

encoder = SimpleEncoder((go_board_rows, go_board_cols))

processor = GoDataProcessor(encoder=encoder.name())

generator = processor.load_go_data('train', num_games, use_generator=True)
test_generator = processor.load_go_data('test', num_games, use_generator=True)

input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
network_layers = small.layers(input_shape)
model = Sequential()
for layer in network_layers:
    model.add(layer)
model.add(Dense(num_classes, activation='softmax'))
optimizer = Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0)
model.summary()
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

epochs = 20
batch_size = 128
model.fit_generator(generator=generator.generate(batch_size, num_classes),
                    epochs=epochs,
                    steps_per_epoch=generator.get_num_samples() / batch_size,
                    validation_data=test_generator.generate(batch_size, num_classes),
                    validation_steps=test_generator.get_num_samples() / batch_size,
                    callbacks=[
                        ModelCheckpoint('./checkpoints/small_model_epoch_{epoch}.h5'),
                        TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=32, write_graph=True,
                                    write_grads=False, write_images=False, embeddings_freq=0,
                                    embeddings_layer_names=None, embeddings_metadata=None, embeddings_data=None,
                                    update_freq='epoch')
                    ])

model.evaluate_generator(generator=test_generator.generate(batch_size, num_classes),
                         steps=test_generator.get_num_samples() / batch_size)
