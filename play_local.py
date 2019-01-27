import h5py

import tensorflow as tf
from dlgo.agent.predict import load_prediction_agent
from dlgo.agent.termination import PassWhenOpponentPasses
from dlgo.gtp.local import LocalGtpBot
from kerasutils import set_gpu_memory_target

if __name__ == "__main__":
    bot = load_prediction_agent(h5py.File("./agents/deep_bot.h5", "r"))
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        set_gpu_memory_target(0.7)
        gnu_go = LocalGtpBot(go_bot=bot, termination=PassWhenOpponentPasses(),
                             handicap=0, opponent='gnugo', )
        gnu_go.run()
