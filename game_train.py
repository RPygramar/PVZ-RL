import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import random
import pickle
import os
import pvz_env

def run_q(episodes, is_training=True, render=False):
    env = gym.make('pvz-rl', render_mode='human' if render else None)

    if(is_training):
        # q = np.zeros((801,801,100,100,env.action_space.n),dtype=np.int8)
        obs_space_shape = env.observation_space.shape
        # q = np.zeros(obs_space_shape + (env.action_space.n,), dtype=np.float64)
        q = np.zeros((0,0,0,0, env.action_space.n),dtype=np.float64)
    else:
        f = open('output_model/pvz-rl.pkl','rb')
        q = pickle.load(f)
        f.close()
    
    learning_rate_a = 0.9
    discount_factor_g = 0.9
    epsilon = 1

    steps_per_episode = np.zeros(episodes)

    step_count = 0
    for i in range(episodes):
        if render:
            print(f'Episode {i}')
        
        state = env.reset()[0]
        terminated = False

        while not terminated:
            
            if is_training and random.random() < epsilon:
                action = env.action_space.sample()
            else:
                q_state_idx = tuple(state)

                action = np.argmax(q[q_state_idx])
            
            new_state, reward, terminated, _, _ = env.step(action)

            q_state_action_idx = tuple(state) + (action,)

            q_new_state_idx = tuple(new_state)
            print(q_state_action_idx)
            if is_training:
                q[q_state_action_idx] = q[q_state_action_idx] + learning_rate_a * (
                    reward + discount_factor_g + np.max(q[q_new_state_idx]) - q[q_state_action_idx]
                )

            state = new_state

            step_count += 1

            if terminated:
                steps_per_episode[i] = step_count
                step_count = 0

        # Decrease epsilon
        epsilon = max(epsilon - 1/episodes, 0)

    env.close()

    # Graph steps
    sum_steps = np.zeros(episodes)
    for t in range(episodes):
        sum_steps[t] = np.mean(steps_per_episode[max(0, t-100):(t+1)]) # Average steps per 100 episodes
    plt.plot(sum_steps)
    plt.savefig('plots/pvz_solution.png')

    if is_training:
        # Save Q Table
        f = open("output_model/pvz-rl.pkl","wb")
        pickle.dump(q, f)
        f.close()
    
if __name__ == '__main__':
    run_q(1000, is_training=True, render=False)
    run_q(1, is_training=False, render=True)