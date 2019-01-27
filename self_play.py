import argparse

import h5py

from dlgo.agent.pg import load_policy_agent
from dlgo.rl.simulate import experience_simulation

from kerasutils import set_gpu_memory_target

set_gpu_memory_target(0.4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning-agent', required=True)
    parser.add_argument('--experience', required=True)
    parser.add_argument('--num-games', type=int, required=True)
    args = parser.parse_args()

    l1 = load_policy_agent(h5py.File(args.learning_agent))
    l2 = load_policy_agent(h5py.File(args.learning_agent))

    experience = experience_simulation(args.num_games, l1, l2)

    with h5py.File(args.experience) as experience_outf:
        experience.serialize(experience_outf)


if __name__ == "__main__":
    main()
