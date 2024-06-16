import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register
from gymnasium.utils.env_checker import check_env

import numpy as np
from game.game import Game
from agent.agent import AgentAction

register(
    id='pvz-rl',
    entry_point='pvz_env:GameEnv',
)

class GameEnv(gym.Env):

    metadata = {"render_modes": ["human"], 'render_fps': 30}

    def __init__(self, grid_rows=9, grid_cols=5, render_mode=None):
        
        self.zombies_killed_counter = 0

        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.render_mode = render_mode

        self.pvz_game = Game(fps=self.metadata['render_fps'])

        self.action_space = spaces.Discrete(len(AgentAction))

        self.observation_space = spaces.Box(
            low=0,
            high=np.array([9*5,2000,9*5,1000]),
            shape=(4,),
            dtype=np.int32
            )
        print(self.observation_space)
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.pvz_game.reset(seed=seed)

        plants_owned = self.pvz_game.agent.get_plants_owned()
        suns = self.pvz_game.agent.get_suns()
        pos = self.pvz_game.agent.get_pos()
        zombies_killed = self.pvz_game.agent.get_zombies_killed()

        plants_owned = np.array(self.encode_plants(self.pvz_game.agent.get_plants_owned()), dtype=np.int32)
        suns = np.array([self.pvz_game.agent.get_suns()], dtype=np.int32)
        pos = np.array(self.pvz_game.agent.get_pos(), dtype=np.int32)
        zombies_killed = np.array([len(self.pvz_game.agent.get_zombies_killed())], dtype=np.int32)

        obs = np.concatenate((plants_owned, suns, pos, zombies_killed))
        print('obs: ',obs)
        info = {}

        if self.render_mode == 'human':
            self.render()

        return obs, info
    
    def step(self, action):
        super().step()
        action = self.pvz_game.agent.perform_action(AgentAction(action))

        reward = 0
        terminated = False

        if self.pvz_game.check_zombies_reached_limit():
            reward -= 100
            terminated = True

        if action == AgentAction.UP:
            initial_pos = self.pvz_game.agent.get_pos()
            self.pvz_game.agent.move_up()
            if initial_pos != self.pvz_game.agent.get_pos():
                reward += 1  # Reward for moving up
            else:
                reward -= 5
        elif action == AgentAction.DOWN:
            initial_pos = self.pvz_game.agent.get_pos()
            self.pvz_game.agent.move_down()
            if initial_pos != self.pvz_game.agent.get_pos():
                reward += 1  # Reward for moving down
            else:
                reward -= 5
        elif action == AgentAction.LEFT:
            initial_pos = self.pvz_game.agent.get_pos()
            self.pvz_game.agent.move_left()
            if initial_pos != self.pvz_game.agent.get_pos():
                reward += 1  # Reward for moving left
            else:
                reward -= 5
        elif action == AgentAction.RIGHT:
            initial_pos = self.pvz_game.agent.get_pos()
            self.pvz_game.agent.move_right()
            if initial_pos != self.pvz_game.agent.get_pos():
                reward += 1  # Reward for moving right
            else:
                reward -= 5
        elif action == AgentAction.PLACE_PEASHOOTER:
            distance_to_zombies = self.pvz_game.agent.get_pos()
            initial_plants_owned = len(self.pvz_game.agent.get_plants_owned())
            self.pvz_game.agent.place_plant(0)
            new_plants_owned = len(self.pvz_game.agent.get_plants_owned()) - initial_plants_owned
            if new_plants_owned > 0 :
                reward += (15 - (distance_to_zombies[0] * 2))  # Reward for placing a Peashooter
            else:
                reward -= 10
        elif action == AgentAction.PLACE_SUNFLOWER:
            distance_to_zombies = self.pvz_game.agent.get_pos()
            initial_plants_owned = len(self.pvz_game.agent.get_plants_owned())
            self.pvz_game.agent.place_plant(1)
            new_plants_owned = len(self.pvz_game.agent.get_plants_owned()) - initial_plants_owned
            if new_plants_owned > 0:
                reward += (10 - (distance_to_zombies[0] * 2))  # Reward for placing a Sunflower
            else:
                reward -= 5
        elif action == AgentAction.COLLECT_SUN:
            initial_suns = self.pvz_game.agent.get_suns()
            self.pvz_game.agent.perform_action(AgentAction.COLLECT_SUN)
            collected_suns = self.pvz_game.agent.get_suns() - initial_suns
            if collected_suns > 0:
                reward += 20  # Reward for each sun collected
            else:
                reward -= 10

        # Hypothetical reward for defeating zombies (this needs implementation based on your game logic)
        new_zombies_killed = len(self.pvz_game.agent.get_zombies_killed()) - self.zombies_killed_counter
        if new_zombies_killed > 0:
            self.zombies_killed_counter = new_zombies_killed
            reward += new_zombies_killed * 20  # Reward for each zombie killed

        #  Check for dead plants and adjust reward if necessary
        initial_plants_owned = len(self.pvz_game.agent.get_plants_owned())
        self.pvz_game.agent.remove_dead_plants()
        new_plants_owned = len(self.pvz_game.agent.get_plants_owned())
        if new_plants_owned < initial_plants_owned:
            reward -= (initial_plants_owned - new_plants_owned) * 20  # Penalty for plant deaths

            
        print('reward: ',reward)

        plants_owned = np.array(self.encode_plants(self.pvz_game.agent.get_plants_owned()), dtype=np.int32)
        suns = np.array([self.pvz_game.agent.get_suns()], dtype=np.int32)
        pos = np.array(self.pvz_game.agent.get_pos(), dtype=np.int32)
        zombies_killed = np.array([len(self.pvz_game.agent.get_zombies_killed())], dtype=np.int32)


        obs = np.concatenate((plants_owned,suns,pos,zombies_killed))

        info = {}

        if self.render_mode == 'human':
            print(AgentAction(action))

        return obs, reward, terminated, False, info

    def render(self):
        self.pvz_game.start_game()

    def encode_plants(self, plants):
        plant_type_map = {
            'Peashooter': 1,
            'Sunflower': 2,
        }
        return [plant_type_map[type(plant).__name__] for plant in plants]

# class GameEnv(gym.Env):

#     metadata = {"render_modes": ["human"], 'render_fps': 30}

#     def __init__(self, grid_rows=9, grid_cols=5, render_mode=None):
#         self.zombies_killed_counter = 0
#         self.grid_rows = grid_rows
#         self.grid_cols = grid_cols
#         self.render_mode = render_mode

#         self.pvz_game = Game(fps=self.metadata['render_fps'])

#         self.action_space = spaces.Discrete(len(AgentAction))

#         # Define the observation space based on actual observation structure
#         self.observation_space = spaces.Box(
#             low=0,
#             high=9*5,  # Define appropriately based on your environment's limits
#             shape=(1,),  # Adjust this to match the total length of obs
#             dtype=np.int32
#         )

#     def reset(self, seed=None, options=None):
#         super().reset(seed=seed)
#         self.pvz_game.reset(seed=seed)

#         plants_owned = self.encode_plants(self.pvz_game.agent.get_plants_owned())
#         suns = np.array([self.pvz_game.agent.get_suns()])
#         pos = self.pvz_game.agent.get_pos()
#         zombies_killed = np.array([len(self.pvz_game.agent.get_zombies_killed())])

#         # Flatten all components into a single array
#         obs = np.concatenate((plants_owned, suns, pos, zombies_killed)).astype(np.int32)

#         # Print for debugging
#         print("Plants Owned:", plants_owned)
#         print("Suns:", suns)
#         print("Position:", pos)
#         print("Zombies Killed:", zombies_killed)
#         print("Combined Observation Shape:", obs.shape)
#         print("Combined Observation:", obs)

#         info = {}

#         if self.render_mode == 'human':
#             self.render()

#         return obs, info

#     def step(self, action):
#         super().step()
#         action = self.pvz_game.agent.perform_action(AgentAction(action))

#         reward = 0
#         terminated = False

#         if self.pvz_game.check_zombies_reached_limit():
#             reward -= 100
#             terminated = True

#         # Similar action handling as before ...

#         # Update observations
#         plants_owned = np.array(self.encode_plants(self.pvz_game.agent.get_plants_owned()), dtype=np.int32)
#         suns = np.array([self.pvz_game.agent.get_suns()], dtype=np.int32)
#         pos = np.array(self.pvz_game.agent.get_pos(), dtype=np.int32)
#         zombies_killed = np.array([len(self.pvz_game.agent.get_zombies_killed())], dtype=np.int32)

#         obs = np.concatenate((plants_owned, suns, pos, zombies_killed)).astype(np.int32)

#         info = {}

#         if self.render_mode == 'human':
#             print(AgentAction(action))

#         return obs, reward, terminated, False, info

#     def render(self):
#         self.pvz_game.start_game()

#     def encode_plants(self, plants):
#         plant_type_map = {
#             'Peashooter': 1,
#             'Sunflower': 2,
#         }
#         return [plant_type_map[type(plant).__name__] for plant in plants]

if __name__ == '__main__':
    env = gym.make('pvz-rl', render_mode='human')

    print('Environment Begin')
    check_env(env.unwrapped)
    print('Environment End')

    obs = env.reset()[0]

    while True:
        rand_action = env.action_space.sample()
        obs, reward, terminated, _, _ = env.step(rand_action)

        if terminated:
            obs = env.reset()[0]
