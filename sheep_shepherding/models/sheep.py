import math
import random
import numpy as np

'''
BASED ON
Analysis of local-camera-based shepherding navigation
Tsunoda et al. 2018
'''

class Sheep: 
    def __init__(self, param,  i):
        #初期化 
        self.R = 20
        self.no = i
        self.p1 = param["sheep_param"][0]
        self.p2 = param["sheep_param"][1]
        self.p3 = param["sheep_param"][2]
        self.p4 = param["sheep_param"][3]
        self.slow = False
        self.farthest = False
        self.position = np.array([0, 0])
        self.velocity = np.array([0, 0])
        self.reset(param, i,  -1)
        
    def print(self):
        print("No.{} pos:{} slow:{}".format(self.no, self.position, self.slow))
    
    def reset(self, param, i, trial):
        '''
        初期位置, 速度のリセット 

        random関数に用いるseed値の更新
        '''
        random.seed(i+trial)
        base_position = np.array(param["sheep_initial_pos_base"])
        r = math.sqrt(random.uniform(0, param["sheep_initial_pos_radius"] ** 2))
        theta = random.uniform(-math.pi, math.pi)
        self.position = base_position + np.array([r * math.cos(theta), r * math.sin(theta)])
        self.velocity = np.array([0, 0])
      
    def slow_param(self, param):
        '''
        遅い羊に設定するときのパラメータ設定
        p1:別の羊からの斥力 p2:別の羊との整列力 p3:別の羊からの引力 p4:牧羊犬からの斥力
        '''
        self.p1 = param["slow_sheep_param"][0]
        self.p2 = param["slow_sheep_param"][1]
        self.p3 = param["slow_sheep_param"][2]
        self.p4 = param["slow_sheep_param"][3]
        self.slow = True

    def repulsive(self, sheeps):
        '''
        範囲内にいる他のsheepからの斥力
        '''
        u = np.array([0,0])
        u1 = np.array([0,0])
        for other in sheeps:
            u = other.position - self.position
            if np.linalg.norm(u) > 1:
                u1 = u1 + (u / np.power(np.linalg.norm(u), 3) )
            else:
                u1 = u1 + u
        return  - u1 / len(sheeps)

    def alignment(self, sheeps):
        '''
        範囲内にいる他のsheepと速度を合わせる
        '''
        u = np.array([0,0])
        u1 = np.array([0,0])
        for other in sheeps:
            u = other.velocity
            if np.linalg.norm(u) > 0.1 :
                u1 = u1 + (u / np.linalg.norm(u))
            else:
                u1 = u1 + u
        return  - u1 / len(sheeps)

    def attractive(self, sheeps):
        '''
        範囲内にいる他のsheepからの引力
        '''
        u = np.array([0,0])
        u1 = np.array([0,0])
        for other in sheeps:
            u = other.position - self.position
            if np.linalg.norm(u) > 1:
                u1 = u1 + (u / np.linalg.norm(u))
            else:
                u1 = u1 + u
        return u1 / len(sheeps)

    def repulsive_from_shepherd(self, shepherd):
        '''
        shepherdからの斥力
        '''
        u = shepherd.position - self.position
        #羊の検知範囲を考慮するかどうか
        #if np.linalg.norm(u) < self.R:
        #    return np.array([0,0])
        u1 = np.array([0,0])
        if np.linalg.norm(u) > 1:
            u1 = - u / np.power(np.linalg.norm(u), 3)
        else:
            u1 = 0
        return u1
    
    def sheeps_in_region(self, sheeps):
        '''
        羊の視界範囲の中(半径20m)の羊を求める
        '''
        in_sheeps = []
        for other in sheeps:
            u = self.position - other.position
            d = np.linalg.norm(u)
            if d < self.R:
                in_sheeps.append(other)

        return in_sheeps
   
    def update(self, sheeps, shepherd, goal):
        '''
        羊1匹ごとの位置,速度の更新
        '''
        others = self.sheeps_in_region(sheeps)
        if len(others) == 0:
            return
        
        v1 = self.repulsive(others)
        v2 = self.alignment(others)
        v3 = self.attractive(others)
        v4 = self.repulsive_from_shepherd(shepherd)

        v = self.p1 * v1 + self.p2 * v2 + self.p3 * v3 + self.p4 * v4
        self.velocity = v 
        self.position = self.position + v 

        far = self.get_farthest_sheep(sheeps, goal)
        
        if far:
            self.farthest = True
            #print("{} is far".format(self.no))
        else:
            self.farthest = False
        
        '''
        if self.position[0] > 50:
            self.position[0] = 50
            #print("No.{} pos({},{}))".format(self.no, self.position[0], self.position[1],v1,v2,v3,v4))

        if self.position[0] < -50:
            self.position[0] = -50

        if self.position[1] < -50:
            self.position[1] = -50

        if self.position[1] > 50:    
            self.position[1] = 50
        '''
    
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
        return max_sheep == self.no