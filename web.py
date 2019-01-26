import h5py

from dlgo.agent.predict import load_prediction_agent
from dlgo.http.server import get_web_app

from keras.backend import clear_session
clear_session()

bot_from_file = load_prediction_agent(h5py.File("./agents/deep_bot.h5", "r"))
web_app = get_web_app({'predict': bot_from_file})
web_app.run()
