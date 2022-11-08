import random
import numpy as np

class Collective_Shepherd:
    def __init__(self, param):
        #初期化
        self.p1 = param["shepherd_param"][0]
        self.p2 = param["shepherd_param"][1]
        self.p3 = param["shepherd_param"][2]
        self.unique_sheep = {}
        self.reset(param)
    
    def reset(self, param):
        '''
        位置, 速度のreset
        '''
        self.first = False
        self.to_goal = False
        self.nearest_sheep = None
        self.farthest_sheep = None
        self.target_slow_sheep = None
        self.collect_success = []
        self.fast_sheeps = []
        self.position = np.array(param["shepherd_initial_pos"])
        self.velocity = np.array([0, 0])

    def attractive(self, sheep):
        '''
        farthest_sheepからの引力  
        '''
        u = sheep.position - self.position
        if np.linalg.norm(u) != 0:
            u = u / np.linalg.norm(u) 
        return  u
    
    def repulsive(self, sheep):
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

    def get_farthest_sheep_fromgoal(self, sheeps, goal):
        '''
        ターゲットにしている遅い羊から最も遠いfarthest sheepのnoを取得
        '''
        max = 0
        max_sheep = 0
        for i in range(len(sheeps)):
            d =  np.linalg.norm(sheeps[i].position - goal)
            if d > max:
                max = d
                max_sheep = i
        return sheeps[max_sheep].no

    def get_farthest_sheep(self, sheeps, slow_sheep):
        '''
        ターゲットにしている遅い羊から最も遠いfarthest sheepのnoを取得
        '''
        max = 0
        max_sheep = 0
        for i in range(len(sheeps)):
            d =  np.linalg.norm(sheeps[i].position - slow_sheep.position)
            if d > max:
                max = d
                max_sheep = i
        return sheeps[max_sheep].no

    def get_slowsheep(self, sheeps):
        '''
        犬から一番近い、遅い羊のnoを求める
        '''    
        #反応する羊のリストを求める
        #fast_sheeps = []
        slow_sheeps = [sheeps[i] for i in range(len(sheeps)) if sheeps[i].slow == True]

        min = 0
        min_sheep = 0
        for i in range(len(slow_sheeps)):
            d =  np.linalg.norm(slow_sheeps[i].position - self.position)
            if d < min:
                min = d
                min_sheep = i
        nearest_fast_sheep = slow_sheeps[min_sheep]
        return slow_sheeps[min_sheep].no
    
    def get_next_slowsheep(self, sheeps, sheep):
        '''
        collectに成功した羊のリストに加えて, 登録されていない遅い羊のリストを返す
        '''
        #slow_sheepsからcollect_successを抜いたもの
        self.collect_success.append(sheep.no)
        self.collect_success = list(set(self.collect_success))     
        slow_sheeps = [sheeps[i] for i in range(len(sheeps)) if sheeps[i].slow == True]
        target_sheeps = [slow_sheeps[i] for i in range(len(slow_sheeps)) if slow_sheeps[i].no not in self.collect_success]
        #print("--success:{} --target:{}".format(self.collect_success, target_sheeps[0].no))
        return target_sheeps

    def plot_describe(self, keyword, sheep):
        '''
        そのときだけplotのマーカーを変える
        '''
        self.unique_sheep[keyword] = sheep

    def is_success(self, sheeps, slow_sheep):
        '''
        羊が一定の範囲内に収まっているかの判定
        '''
        success = True
        for i in range(len(sheeps)):
            u = sheeps[i].position - slow_sheep.position
            d = np.linalg.norm(u)
            if d > 15:
                success = False
        return success
        
    def collective_move2(self, sheeps, goal):
        '''
        集める動作をする
        '''
        slow_sheeps = [sheeps[i] for i in range(len(sheeps)) if sheeps[i].slow == True]
        
        #最初1step目ではsheepsから遅い羊を見つける
        if self.first == False:
            self.target_slow_sheep = self.get_farthest_sheep_fromgoal(slow_sheeps, goal)
            self.farthest_sheep = self.get_farthest_sheep(self.fast_sheeps, sheeps[self.target_slow_sheep])
            #(self.fast_sheeps)
            self.first = True

        if self.to_goal:
            self.farthest_sheep = self.get_farthest_sheep_fromgoal(sheeps, goal)
        else: #
            ap = [sheeps[i] for i in range(len(sheeps)) if sheeps[i].no in self.collect_success]
            self.farthest_sheep = self.get_farthest_sheep(self.fast_sheeps + ap, sheeps[self.target_slow_sheep])

        self.plot_describe("m", sheeps[self.target_slow_sheep])
        self.plot_describe("b", sheeps[self.farthest_sheep])

        #すべての「反応する羊」がターゲットとする「反応しない羊」の一定の距離まで近づくと次の「反応しない羊」に変える
        if self.is_success(self.fast_sheeps, sheeps[self.target_slow_sheep]):           
            #次の候補を見つける
            self.collect_success.append(sheeps[self.target_slow_sheep].no)  
            candidate_sheeps = []   
            candidate_sheeps = [slow_sheeps[i] for i in range(len(slow_sheeps)) if slow_sheeps[i].no not in self.collect_success]

            if len(candidate_sheeps) == 0:
                self.to_goal = True
                #print("-to goal-")
                return
            #print("-target changed-")
            #print(self.collect_success)
            self.target_slow_sheep = self.get_farthest_sheep_fromgoal(candidate_sheeps, goal)

    def collective_move(self, sheeps, goal):
        '''
        集める動作をする
        '''
        slow_sheeps = [sheeps[i] for i in range(len(sheeps)) if sheeps[i].slow == True]
        
        #最初1step目ではsheepsから遅い羊を見つける
        if self.first == False:
            self.target_slow_sheep = self.get_farthest_sheep_fromgoal(slow_sheeps, goal)
            self.farthest_sheep = self.get_farthest_sheep(self.fast_sheeps, sheeps[self.target_slow_sheep])
            #(self.fast_sheeps)
            self.first = True

        if self.to_goal:
            self.farthest_sheep = self.get_farthest_sheep_fromgoal(sheeps, goal)
        else: #
            ap = [sheeps[i] for i in range(len(sheeps)) if sheeps[i].no in self.collect_success]
            self.farthest_sheep = self.get_farthest_sheep(self.fast_sheeps + ap, sheeps[self.target_slow_sheep])

        self.plot_describe("b", sheeps[self.target_slow_sheep])
        self.plot_describe("y", sheeps[self.farthest_sheep])

        #すべての「反応する羊」がターゲットとする「反応しない羊」の一定の距離まで近づくと次の「反応しない羊」に変える
        if self.is_success(self.fast_sheeps, sheeps[self.target_slow_sheep]):           
            #次の候補を見つける
            self.collect_success.append(sheeps[self.target_slow_sheep].no)  
            candidate_sheeps = []   
            candidate_sheeps = [slow_sheeps[i] for i in range(len(slow_sheeps)) if slow_sheeps[i].no not in self.collect_success]

            if len(candidate_sheeps) == 0:
                self.to_goal = True
                #print("-to goal-")
                return
            #print("-target changed-")
            #print(self.collect_success)
            self.target_slow_sheep = self.get_near_sheep(candidate_sheeps, sheeps[self.target_slow_sheep])
           
    def get_near_sheep(self, sheeps, sheep):
        '''
        当該の羊から一番近い、遅い羊のnoを求める
        '''    
        min = 100
        min_sheep = 0
        for i in range(len(sheeps)):
            d =  np.linalg.norm(sheeps[i].position - sheep.position)
            if d < min:
                min = d
                min_sheep = i
        nearest_fast_sheep = sheeps[min_sheep]
   
        return sheeps[min_sheep].no

    def update(self, sheeps, goal):
        '''
        牧羊犬の位置,速度の更新
        '''
        if len(sheeps) == 0:
            return
        
        self.fast_sheeps = [sheeps[i] for i in range(len(sheeps)) if sheeps[i].slow == False]
        self.collective_move(sheeps ,goal)        
        
        v1 = self.attractive(sheeps[self.farthest_sheep])
        v2 = self.repulsive(sheeps[self.farthest_sheep])
        if self.to_goal == True:
            v3 = self.repulsive_from_goal(goal)
        else:
            v3 = self.repulsive_from_goal(sheeps[self.target_slow_sheep].position)

        v = self.p1 * v1 + self.p2 * v2 + self.p3 * v3
        self.velocity = v 
        self.position = self.position + v

        #print("d:{} v:{}".format(np.linalg.norm(sheeps[self.nearest_sheep].position - sheeps[self.farthest_sheep].position), v))