import argparse

import h5py

from dlgo.agent.q_agent import QAgent
from dlgo.encoders.base import get_encoder_by_name
from dlgo.networks.two_inputs import build_model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', type=int, default=19)
    parser.add_argument('--network', default='large')
    parser.add_argument('--hidden-size', type=int, default=512)
    parser.add_argument('output_file')
    args = parser.parse_args()

    encoder = get_encoder_by_name('simple', args.board_size)
    model = build_model(encoder)

    new_agent = QAgent(model, encoder)
    with h5py.File(args.output_file, 'w') as outf:
        new_agent.serialize(outf)


if __name__ == '__main__':
    main()
