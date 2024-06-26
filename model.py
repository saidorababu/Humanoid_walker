import sys
from sac import SAC
#sys.path.append(r'C:/Users/MPR/miniconda3/Lib/site-packages')
import gymnasium as gym
import os
import argparse

model_dir = "models"
log_dir = "logs"
os.makedirs(model_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

def train(env):
    model = SAC('MlpPolicy', env, verbose=1, device='cpu', tensorboard_log=log_dir)
    TIMESTEPS = 25000
    iters = 0
    while True:
        iters += 1
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)
        model.save(f"{model_dir}"/"SAC_{TIMESTEPS*iters}")

def test(env, path_to_model):
    model = SAC.load(path_to_model, env=env)
    obs = env.reset()[0]
    done = False
    extra_steps = 500
    while True:
        action, _ = model.predict(obs)
        obs, _, done, _, _ = env.step(action)

        if done:
            extra_steps -= 1

            if extra_steps < 0:
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train or test model.')
    parser.add_argument('gymenv', help='Gymnasium environment i.e. Humanoid-v4')
    parser.add_argument('-t', '--train', action='store_true')
    parser.add_argument('-s', '--test', metavar='path_to_model')
    args = parser.parse_args()
    
    if args.train:
        print("Works")
        gymenv = gym.make(args.gymenv, render_mode=None)
        train(gymenv)

    if(args.test):
        if os.path.isfile(args.test):
            gymenv = gym.make(args.gymenv, render_mode='human')
            test(gymenv,path_to_model=args.test)
        else:
            print(f'{args.test} not found.')