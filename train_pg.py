import argparse

import h5py

from dlgo.agent.pg import load_policy_agent
from dlgo.rl.experience import load_experience

from kerasutils import set_gpu_memory_target

set_gpu_memory_target(0.4)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning-agent', required=True)
    parser.add_argument('--agent-out', required=True)
    parser.add_argument('--lr', type=float, default=0.01)
    parser.add_argument('--bs', type=int, default=512)
    parser.add_argument('experience', nargs='+')

    args = parser.parse_args()

    learning_agent = load_policy_agent(h5py.File(args.learning_agent))
    for exp_filename in args.experience:
        print('Training with %s...' % exp_filename)
        exp_buffer = load_experience(h5py.File(exp_filename))
        learning_agent.train(exp_buffer, lr=args.lr, batch_size=args.bs)

    with h5py.File(args.agent_out, 'w') as updated_agent_outf:
        learning_agent.serialize(updated_agent_outf)


if __name__ == '__main__':
    main()
