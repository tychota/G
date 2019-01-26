from typing import Dict, Any

import numpy as np
from h5py import File
from keras import Model

import kerasutils
from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo.encoders.base import Encoder, get_encoder_by_name
from dlgo.goboard_fast import GameState, Move


class DeepLearningAgent(Agent):
    def __init__(self, model: Model, encoder: Encoder):
        super(DeepLearningAgent, self).__init__()
        self.model = model
        self.encoder = encoder

    def predict(self, game_state):
        encoded_state = self.encoder.encode(game_state)
        input_tensor = np.array([encoded_state])
        return self.model.predict(input_tensor)[0]

    def select_move(self, game_state: GameState):
        num_moves = self.encoder.board_width * self.encoder.board_height
        move_probs = self.predict(game_state)

        move_probs = move_probs ** 3
        eps = 1e-6
        move_probs = np.clip(move_probs, eps, 1 - eps)
        move_probs /= np.sum(move_probs)

        candidates = np.arange(num_moves)
        ranked_move = np.random.choice(
            candidates,
            num_moves,
            replace=False,
            p=move_probs
        )
        for point_idx in ranked_move:
            point = self.encoder.decode_point_index(point_idx)
            is_valid_move = game_state.is_valid_move(Move.play(point))
            is_not_stupid_move = not is_point_an_eye(game_state.board, point, game_state.next_player)
            if is_valid_move and is_not_stupid_move:
                return Move.play(point)
        return Move.pass_turn()

    def serialize(self, h5file: File):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self.encoder.name()
        h5file['encoder'].attrs['board_width'] = self.encoder.board_width
        h5file['encoder'].attrs['board_height'] = self.encoder.board_height
        h5file.create_group('model')
        kerasutils.save_model_to_hdf5_group(self.model, h5file['model'])


def load_prediction_agent(h5file: File):
    model = kerasutils.load_model_from_hdf5_group(h5file['model'])
    encoder_name = h5file['encoder'].attrs['name']
    if not isinstance(encoder_name, str):
        encoder_name = encoder_name.decode('ascii')
    board_width = h5file['encoder'].attrs['board_width']
    board_height = h5file['encoder'].attrs['board_height']
    encoder = get_encoder_by_name(
        encoder_name, (board_width, board_height))
    return DeepLearningAgent(model, encoder)
