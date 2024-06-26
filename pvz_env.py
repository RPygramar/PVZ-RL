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

    metadata = {"render_modes": ["human"], 'render_fps': 144}

    def __init__(self, grid_rows=10, grid_cols=5, render_mode=None):

        self.zombies_killed_counter = 0

        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.render_mode = render_mode

        self.pvz_game = Game(fps=self.metadata['render_fps'])

        self.action_space = spaces.Discrete(len(AgentAction))

        self.observation_space = spaces.Dict({
            "board": spaces.Box(low=0, high=3, shape=(10, 5), dtype=np.int32),
            #"position": spaces.Box(low=0, high=1, shape=(9,5), dtype=np.int32)
            #"suns": spaces.Box(low=0, high=np.inf, dtype=np.int32)
        })

        # print(self.observation_space)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.pvz_game.reset(seed=seed)

        self.zombies_killed_counter = 0

        board = self.encode_board()
        # suns = [self.pvz_game.agent.get_suns()]
        # pos = self.encode_pos_agent()

        obs = {"board": board}#, "position" : pos}#, "suns": suns}
        info = {}

        if self.render_mode == 'human':
            self.render()
        # print('obs: ', obs)
        return obs, info
    
    def step(self, action):
        # super().step(action)
        action = self.pvz_game.agent.perform_action(AgentAction(action))

        board = self.encode_board()
        # suns = [self.pvz_game.agent.get_suns()]
        # pos = self.encode_pos_agent()

        reward = 0
        terminated = False
        if self.pvz_game.check_zombies_reached_limit():
            reward -= 100
            terminated = True
            #print(self.pvz_game.agent.get_pos())
            #print(board)
            self.zombies_killed_counter = 0
            #print(board)
        if self.pvz_game.agent.get_suns() >= 10000:
            reward += 100
            terminated = True
            #print(self.pvz_game.agent.get_pos())
            self.zombies_killed_counter = 0
            #print(board)
        
        if self.zombies_killed_counter >= 100:
            reward += 100
            terminated = True
        
        if action == AgentAction.UP.value:
            initial_pos = self.pvz_game.agent.get_pos()
            self.pvz_game.agent.move_up()
            if initial_pos != self.pvz_game.agent.get_pos():
                reward += 0  # Reward for moving up
            else:
                reward -= 5
        elif action == AgentAction.DOWN.value:
            initial_pos = self.pvz_game.agent.get_pos()
            self.pvz_game.agent.move_down()
            if initial_pos != self.pvz_game.agent.get_pos():
                reward += 0  # Reward for moving down
            else:
                reward -= 5
        elif action == AgentAction.LEFT.value:
            initial_pos = self.pvz_game.agent.get_pos()
            self.pvz_game.agent.move_left()
            if initial_pos != self.pvz_game.agent.get_pos():
                reward += 0  # Reward for moving left
            else:
                reward -= 5
        elif action == AgentAction.RIGHT.value:
            initial_pos = self.pvz_game.agent.get_pos()
            self.pvz_game.agent.move_right()
            if initial_pos != self.pvz_game.agent.get_pos():
                reward += 0  # Reward for moving right
            else:
                reward -= 5
        elif action == AgentAction.PLACE_PEASHOOTER.value:
            distance_to_zombies = self.pvz_game.agent.get_pos()
            self.pvz_game.agent.place_plant(0)
            plant = self.pvz_game.agent.get_plants_owned()[-1]
            new_plants_owned = self.pvz_game.agent.final_plants_value - self.pvz_game.agent.initial_plants_value
            if new_plants_owned > 0 and (3 == board[-1][plant.get_pos()[1]]):
                reward += (25 - (distance_to_zombies[0] * 2))  # Reward for placing a Peashooter
                # print(distance_to_zombies, reward)
                # print('reward peashooter: ',reward)
            else:
                reward -= 3
        # elif action == AgentAction.PLACE_SUNFLOWER.value:
        #     distance_to_zombies = self.pvz_game.agent.get_pos()
        #     self.pvz_game.agent.place_plant(1)
        #     plant = self.pvz_game.agent.get_plants_owned()[-1]
        #     new_plants_owned = self.pvz_game.agent.final_plants_value - self.pvz_game.agent.initial_plants_value
        #     if new_plants_owned > 0 and not (3 == board[-1][plant.get_pos()[1]]):
        #         reward += (5 - (distance_to_zombies[0] * 2))  # Reward for placing a Sunflower
        #         # print('reward sunflower: ',reward)
        #     else:
        #         reward -= 3

        elif action == AgentAction.COLLECT_SUN.value:
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
            reward += new_zombies_killed * 2  # Reward for each zombie killed
        print('zombies: ',new_zombies_killed)
        #  Check for dead plants and adjust reward if necessary
        # initial_plants_owned = self.pvz_game.agent.initial_plants_value
        # self.pvz_game.agent.remove_dead_plants()
        # new_plants_owned = self.pvz_game.agent.final_plants_value
        # if new_plants_owned < initial_plants_owned:
        #     reward -= (initial_plants_owned - new_plants_owned) * 10  # Penalty for plant deaths
            
        # print('reward: ',reward)
        # print(board)
        obs = {"board": board}#, "position": pos}#, "suns": suns}
        info = {}
        if self.render_mode == 'human':
            self.render()
            # print(AgentAction(action))
        return obs, reward, terminated, False, info
    
    def render(self):
        self.pvz_game.start_game()

    def encode_plants(self, plants):
        plant_type_map = {
            'Peashooter': 1,
            'Sunflower': 2,
        }
        return [plant_type_map[type(plant).__name__] for plant in plants]
    
    def encode_board(self):
        board = np.zeros((self.grid_rows, self.grid_cols), dtype=np.int32)
        # print(board)
        for plant in self.pvz_game.agent.get_plants_owned():
            x, y = plant.get_pos()
            if type(plant).__name__ == "Peashooter":
                board[x, y] = 1
            elif type(plant).__name__ == "Sunflower":
                board[x, y] = 2
        for zombie in self.pvz_game.horde.get_horde():
            x, y = zombie.get_pos()
            # print(x,y)
            board[x, y] = 3
        # print(board)
        return board.tolist()
    
    def encode_pos_agent(self):
        board = np.zeros((self.grid_rows-1, self.grid_cols-1), dtype=np.int32)
        x, y = self.pvz_game.agent.get_pos()
        board[x, y] = 1
        return board.tolist()
    
if __name__ == '__main__':
    env = gym.make('pvz-rl', render_mode='human')

    # print('Environment Begin')
    check_env(env.unwrapped)
    # print('Environment End')

    obs = env.reset()[0]

    while True:
        rand_action = env.action_space.sample()
        obs, reward, terminated, _, _ = env.step(rand_action)
        if terminated:
            obs = env.reset()[0]