#!/usr/bin/env python3
from dlgo.gtp.frontend import GTPFrontend
from dlgo.agent.ac_agent import load_ac_agent
from dlgo.agent import termination
import h5py

from kerasutils import set_gpu_memory_target

set_gpu_memory_target(0.3)

# model_file = h5py.File("agents/deep_bot.h5", "r")
model_file = h5py.File("./bots/ac_01048000.hdf5", "r")
agent = load_ac_agent(model_file)
strategy = termination.get("opponent_passes")
termination_agent = termination.TerminationAgent(agent, strategy)


frontend = GTPFrontend(termination_agent)
frontend.run()
