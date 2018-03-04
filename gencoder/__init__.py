import importlib


def get_encoder_by_name(name: str, board_size):
    if isinstance(board_size, int):
        board_size = (board_size, board_size)
    mod = importlib.import_module("gencoder." + name)
    constructor = getattr(mod, 'create')
    return constructor(board_size)