#!/usr/bin/env python3
from dlgo.gtp.frontend import GTPFrontend
from dlgo.agent.predict import load_prediction_agent
from dlgo.agent import termination
import h5py

from kerasutils import set_gpu_memory_target

set_gpu_memory_target(0.4)

# model_file = h5py.File("agents/deep_bot.h5", "r")
model_file = h5py.File("agents/learning_9x9_003.h5", "r")
agent = load_prediction_agent(model_file)
strategy = termination.get("opponent_passes")
termination_agent = termination.TerminationAgent(agent, strategy)


frontend = GTPFrontend(termination_agent)
frontend.run()
