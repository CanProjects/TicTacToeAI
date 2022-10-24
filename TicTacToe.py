from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random
import copy
from stable_baselines3 import PPO
import stable_baselines3

class TicTacToe(Env):

    def __init__(self):
        self.action_space = Discrete(9)
        self.observation_space = Box(0,2, shape = (3,3), dtype = np.int32)
        self.board = np.zeros((3,3),np.int)
        self.done = False
        
    def step(self, action):
        #If coordinates are failing, delete this line
        # action = action + 1
        info = {}
        across = action % 3 
        down = (action - across) / 3
        #Puts the move in
        if self.board[int(down)][across] != 0:
            # print('illegal')
            reward = -15
            self.done = True
            return self.board,reward,self.done,info
                
        self.board[int(down)][across] = 1
        self.render()

        if self.winCheck() == 1:
            reward = 1
            self.done = True
            # print('X win')
            return self.board,reward,self.done,info

        if self.winCheck() == 4:
            reward = 0
            self.done = True
            # print('Draw')
            return self.board,reward,self.done,info



        #This lets random play player 2 ############

        # legal = False
        # while not legal:
        #     index1 = random.randint(0,2)
        #     index2 = random.randint(0,2)
        #     if self.board[index1][index2] == 0:
        #         self.board[index1][index2] = 2
        #         legal = True

        ############# This lets you play player 2

        actionO = int(input('Your move? '))              
        across = actionO % 3 
        down = (actionO - across) / 3
        #Puts the move in
        self.board[int(down)][across] = 2


        ######################################
        if self.winCheck() == 2:
            # print('O win')
            reward = -10
            self.done = True
            return self.board,reward,self.done,info

        reward = 0 
        info = {}
        self.done = False
        
        return self.board,reward,self.done,info

    def winCheck(self):

        if self.board[0][0] != 0 and self.board[0][1] != 0 and self.board[0][2] != 0 and self.board[1][0] != 0 and self.board[1][1] != 0 and self.board[1][2] != 0 and self.board[2][0] != 0 and self.board[2][1] != 0 and self.board[2][2] != 0:
            return 4

        #Across 
        for i in self.board:
            if i[0] == 1 and i[1] == 1 and i[2] == 1:
                return 1
            if i[0] == 2 and i[1] == 2 and i[2] == 2:
                return 2

        #down
        if self.board[0][0] == 1 and self.board[1][0] == 1 and self.board[2][0] == 1:
            return 1
        if self.board[0][1] == 1 and self.board[1][1] == 1 and self.board[2][1] == 1:
            return 1
        if self.board[0][2] == 1 and self.board[1][2] == 1 and self.board[2][2] == 1:
            return 1

        if self.board[0][0] == 2 and self.board[1][0] == 2 and self.board[2][0] == 2:
            return 2
        if self.board[0][1] == 2 and self.board[1][1] == 2 and self.board[2][1] == 2:
            return 2
        if self.board[0][2] == 2 and self.board[1][2] == 2 and self.board[2][2] == 2:
            return 2

        #diagnols

        if self.board[0][0] == 1 and self.board[1][1] == 1 and self.board[2][2] == 1:
            return 1 
        if self.board[0][0] == 2 and self.board[1][1] == 2 and self.board[2][2] == 2:
            return 2

        if self.board[0][2] == 1 and self.board[1][1] == 1 and self.board[2][0] == 1:
            return 1 
        if self.board[0][2] == 2 and self.board[1][1] == 2 and self.board[2][0] == 2:
            return 2

        return 0 

    def render(self):
        printList = []
        for i in self.board:
            for z in i:
                if z == 0:
                    printList.append('[ ]')
                if z == 1:
                    printList.append('[X]')
                if z == 2:
                    printList.append('[0]')

        print(printList[0],printList[1],printList[2])
        print(printList[3],printList[4],printList[5])
        print(printList[6],printList[7],printList[8])
        print()
        pass

    def reset(self):
        self.board = np.zeros((3,3))
        self.done = False
        return self.board




env = TicTacToe()


######################### (This is for you to play, no AI)
# done = False
# env.render()

# while not done:
    
#     action = int(input('Move? '))
#     obs, rewards, done, info = env.step(action)
#     env.render()


####################### (This is for AI to Learn )

# model = PPO('MlpPolicy', env, verbose=1)
# model.learn(total_timesteps=200000)
# model.save("TicTacToe")


######################## (This is to view AI Play)

model = PPO.load("TicTacToe")

obs = env.reset()
done = False

while not done:
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
