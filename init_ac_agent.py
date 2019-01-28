import argparse

import h5py

from keras.layers import Dense, Input, Conv2D, Flatten
from keras.models import Model
from dlgo.agent.ac_agent import ACAgent
from dlgo.encoders.base import get_encoder_by_name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', type=int, default=19)
    # parser.add_argument('--network', default='large')
    parser.add_argument('--hidden-size', type=int, default=512)
    parser.add_argument('output_file')
    args = parser.parse_args()

    encoder = get_encoder_by_name('simple', args.board_size)
    board_input = Input(shape=encoder.shape(), name='board_input')

    # processed_board = board_input
    # network = getattr(dlgo.networks, args.network)
    # for layer in network.layers(encoder.shape()):
    #     processed_board = layer(processed_board)

    conv1 = Conv2D(64, (7, 7), padding='same', activation='relu', name='conv1')(board_input)
    conv2 = Conv2D(64, (3, 3), padding='same', activation='relu', name='conv2')(conv1)
    conv3 = Conv2D(64, (3, 3), padding='same', activation='relu', name='conv3')(conv2)
    conv4 = Conv2D(48, (3, 3), padding='same', activation='relu', name='conv4')(conv3)
    conv5 = Conv2D(32, (3, 3), padding='same', activation='relu', name='conv5')(conv4)
    conv6 = Conv2D(32, (3, 3), padding='same', activation='relu', name='conv6')(conv5)

    flat = Flatten(name='flat')(conv6)
    processed_board = Dense(args.hidden_size, activation='relu')(flat)

    policy_hidden_layer = Dense(args.hidden_size, activation='relu')(processed_board)
    policy_output = Dense(encoder.num_points(), activation='softmax', name='policy')(policy_hidden_layer)

    value_hidden_layer = Dense(args.hidden_size, activation='relu')(processed_board)
    value_output = Dense(1, activation='tanh', name='value')(value_hidden_layer)

    model = Model(inputs=[board_input], outputs=[policy_output, value_output])

    new_agent = ACAgent(model, encoder)
    with h5py.File(args.output_file, 'w') as outf:
        new_agent.serialize(outf)


if __name__ == '__main__':
    main()
