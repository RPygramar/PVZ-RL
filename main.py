import random
from game.game import Game
from agent.agent import AgentAction

if __name__ == '__main__':
    game = Game()
    game.start_game()
    while True:
        rand_action = random.choice(list(AgentAction))
        #print(rand_action)

        game.agent.perform_action(rand_action)
        game.start_game()