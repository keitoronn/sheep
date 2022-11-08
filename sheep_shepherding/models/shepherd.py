import random
import numpy as np

'''
BASED ON
Analysis of local-camera-based shepherding navigation
Tsunoda et al. 2018
'''

class Shepherd:
    def __init__(self, param):
        #初期化
        self.p1 = param["shepherd_param"][0]
        self.p2 = param["shepherd_param"][1]
        self.p3 = param["shepherd_param"][2]
        self.unique_sheep = {}
        self.position = np.array([0,0])
        self.velocity = np.array([0,0])
        self.reset(param)
    
    def reset(self, param):
        '''
        位置, 速度のreset
        '''
        self.position = np.array(param["shepherd_initial_pos"])
        self.velocity = np.array([random.uniform(0, 2),  random.uniform(0, 2)])

    def attractive(self, sheep, goal):
        '''
        farthest_sheepからの引力  
        '''
        u = sheep.position - self.position
        if np.linalg.norm(u) != 0:
            u = u / np.linalg.norm(u) 
        return  u
    
    def repulsive(self, sheep, goal):
        '''
        farthest_sheepからの斥力
        '''
        u = sheep.position - self.position
        if np.linalg.norm(u) != 0:
            u = - u / np.power(np.linalg.norm(u), 3) 
        return  u
  
    def repulsive_from_goal(self, goal):
        '''
        goalポイントからの斥力
        '''
        u = goal - self.position 
        if np.linalg.norm(u) != 0:
            u = - u / np.linalg.norm(u)
        return u

    def plot_describe(self, keyword, sheep):
        '''
        そのときだけplotのマーカーを変える
        '''
        self.unique_sheep[keyword] = sheep

    def get_farthest_sheep(self, sheeps, goal):
        '''
        ゴールから最も遠いfarthest sheepを取得
        '''
        max = 0
        max_sheep = 0
        for i in range(len(sheeps)):
            d =  np.linalg.norm(sheeps[i].position - goal)
            if d > max:
                max = d
                max_sheep = i
        return sheeps[max_sheep]
            
   
    def update(self, sheeps, goal):
        '''
        牧羊犬の位置,速度の更新
        '''
        #v1=v2=v3 = [0,0]
        if len(sheeps) == 0:
            return
        farthest_sheep = self.get_farthest_sheep(sheeps, goal)
        self.plot_describe("b", farthest_sheep)

        v1 = self.attractive(farthest_sheep, goal)
        v2 = self.repulsive(farthest_sheep, goal)
        v3 = self.repulsive_from_goal(goal)

        v = self.p1 * v1 + self.p2 * v2 + self.p3 * v3
        self.velocity = v 
        self.position = self.position + v