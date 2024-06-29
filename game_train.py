import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import random
import pickle as pkl
import os
import pvz_env

def convert_state(state):
    """ Convert state representation to a hashable type (tuples). """
    board = tuple(map(tuple, state['board']))
    #position = tuple(map(tuple, state['position']))
    #suns = tuple(state['suns'])
    return ('board', board)#, ('position', position)#, ('suns', suns)

def check_pair_existence(q_table, state, action):
    """ Check if the state-action pair exists in the Q-table. """
    return (state, action) in q_table

def run_q(episodes, is_training=True, render=False):
    env = gym.make('pvz-rl', render_mode='human' if render else None)
    
    action_space = env.action_space.n

    q_table = {}

    if not is_training:
        with open('output_model/pvz-rl.pkl', 'rb') as f:
            q_table = pkl.load(f)

    learning_rate = 0.9
    discount_factor = 0.9
    epsilon = 1

    steps_per_episode = np.zeros(episodes)

    for episode in range(episodes):
        if render:
            # print(f'---- EPISODE {episode + 1} ----')
            pass

        state, _ = env.reset()
        state = convert_state(state)
        terminated = False
        step_count = 0
        total_reward = 0

        while not terminated:
            step_count += 1

            if is_training and random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table.get(state, np.zeros(action_space)))

            new_state, reward, terminated, _, _ = env.step(action)
            new_state = convert_state(new_state)
            
            if is_training:
                q_table[(state, action)] = q_table.get((state, action), 0) + learning_rate * (reward + discount_factor * np.max([q_table.get((new_state, a), 0) for a in range(action_space)]) - q_table.get((state, action), 0))
                
            state = new_state
            total_reward += reward

            if terminated:
                print(f'---- EPISODE {episode + 1} ----')
                print('total_reward: ', total_reward)
                print('Epsilon: ',epsilon)
                print('Step Count:', step_count)
                print('Final State:', state)
                steps_per_episode[episode] = step_count

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
        with open("output_model/pvz-rl.pkl", "wb") as f:
            pkl.dump(q_table, f)

if __name__ == '__main__':
    run_q(500, is_training=True, render=True)
    run_q(1, is_training=False, render=True)
