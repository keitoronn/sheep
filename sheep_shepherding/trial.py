from . import models
from . import util
from .util import analyze_shelve
from .util import plot_ss as plt
from .util import gzshelve
from .models import select_shepherd_model

import os
import copy
import csv
import numpy as np

class Trial:
    def __init__(self, param, directory_path):
        '''
        コマンドライン引数とパラメータの取得, ログの保存場所の設定
        '''
        self.param = param
        self.sheep_number = param["sheep_number"]
        self.shepherd_model = param["shepherd_model"]
        self.trials = param["trial_number"]
        self.n_iter = param["n_iter"]
        self.goal = param["goal"]
        self.radius =  param["goal_radius"]
        self.directory_path = directory_path
        self.file_path_ite = directory_path + "/data/{}t{}.db" #iterationごとに保存するファイル
        self.file_path_tri = directory_path + "/data/{}.db" #trialごとに保存するファイル
        self.file_path_ite_csv = directory_path + "/data/{}t{}.csv" #iterationごとに保存するcsvファイル
        self.file_path_tri_csv = directory_path + "/data/{}.csv" #trialごとに保存するファイル

    def write_line(self, db, key, value):
        db[str(key)] = value

    def update(self, sheeps, shepherd, goal):
        '''
        1stepごとに羊,牧羊犬の座標などを更新
        '''
        #tmp = [sheeps[i] for i in range(len(sheeps))]
        tmp = copy.deepcopy(sheeps)
        max = 0
        max_sheep = 0
        [sheeps[i].update(tmp, shepherd, goal) for i in range(len(sheeps))]
        shepherd.update(tmp, goal)    

    def is_success(self, sheeps):
        '''
        羊がゴールの範囲内に収まっているかの判定
        '''
        success = True
        for i in range(len(sheeps)):
            u = sheeps[i].position - self.goal
            d = np.linalg.norm(u)
            if d > self.radius:
                success = False
        return success
    
    def demo(self, slow_num, trial):
        '''
        1trialのループ　shelveファイルへの保存
        '''            
        print("demo")
        #sheepsの初期化
        sheeps = [models.sheep.Sheep(self.param, i) for i in range(0, self.sheep_number)]
        [sheeps[i].slow_param(self.param) for i in range(0, slow_num)]
        #初期位置の設定
        [sheeps[i].reset(self.param, i, trial) for i in range(len(sheeps))]

        #shepherdの初期化
        shepherd_in = select_shepherd_model(self.shepherd_model, self.param)

        fig, ax = plt.init_figure()
        plt.init_plot_line(ax, self.param, sheeps, shepherd_in)
        
        ###
        success = 0
        for t in range(0, self.n_iter):
            plt.plot_per_iteration(ax, t, sheeps, shepherd_in, True)
            fig.savefig('{}/png/{}.png'.format(self.directory_path, t))
            self.update(sheeps, shepherd_in, self.goal)
                
            if self.is_success(sheeps) == True: #誘導が成功すると途中でシミュレーション終了
                success = 1
                break
        ###
        return t, success

    def loop(self, slow_num):
        '''
        self.trial回の繰り返し
        '''
        #sheepsの初期化
        sheeps = [models.sheep.Sheep(self.param, i) for i in range(0, self.sheep_number)]
        [sheeps[i].slow_param(self.param) for i in range(0, slow_num)]

        #shepherdの初期化
        shepherd_in = select_shepherd_model(self.shepherd_model, self.param)

        success_rate = 0

        for trial in range(0, self.trials):
            end_time, success = self.trial_loop(self.file_path_ite.format(slow_num, trial), sheeps, shepherd_in) 
            success_rate = success_rate + success

            # 終了時の時刻を記録
            with gzshelve.open(self.file_path_tri.format(slow_num)) as db:
                self.write_line(db, trial, [end_time, sheeps, shepherd_in])
            
            [sheeps[i].reset(self.param, i, trial) for i in range(len(sheeps))]
            shepherd_in.reset(self.param)
        
        return success_rate

    def trial_loop(self, file_path, sheeps, shepherd_in):
        '''
        1trialのループ　shelveファイルへの保存
        '''            
        db = gzshelve.open(file_path)
        ###
        success = 0
        for t in range(0, self.n_iter):
            self.write_line(db, t, [sheeps, shepherd_in])
            self.update(sheeps, shepherd_in, self.goal)
                
            if self.is_success(sheeps) == True: #誘導が成功すると途中でシミュレーション終了
                success = 1
                break
        ###
        db.close()
        return t, success

    def trial_loop_experimental(self, slow_num, trial):
        '''
        1trialのループ　shelveファイルへの保存
        '''            
        #sheepsの初期化
        sheeps = [models.sheep.Sheep(self.param, i) for i in range(0, self.sheep_number)]
        [sheeps[i].slow_param(self.param) for i in range(0, slow_num)]
        #初期位置の設定
        [sheeps[i].reset(self.param, i, trial) for i in range(len(sheeps))]

        #shepherdの初期化
        shepherd_in = select_shepherd_model(self.shepherd_model, self.param)

        #shelveファイルを開きながらiterationを回す
        try:
            db = gzshelve.open(self.file_path_ite.format(slow_num, trial))
        except Exception as e:
            print(e)
            print("file_path:{}".format(os.path.abspath(self.file_path_ite.format(slow_num, trial))))
        
        ###
        success = 0
        for t in range(0, self.n_iter):
            self.write_line(db, t, [sheeps, shepherd_in])
            self.update(sheeps, shepherd_in, self.goal)
                
            if self.is_success(sheeps) == True: #誘導が成功すると途中でシミュレーション終了
                success = 1
                break
        ###
        db.close()

        # 終了時の時刻と羊,牧羊犬の位置を記録(waitが必要だが未実装)
        #with gzshelve.open(self.file_path_tri.format(slow_num)) as db:
        #    self.write_line(db, trial, [t, sheeps, shepherd_in])
        return (slow_num, success)

### ここからcsv保存の場合のメソッド ###

    def loop_csv(self, slow_num):
        '''
        self.trial回の繰り返し
        '''
        #sheepsの初期化
        sheeps = [models.sheep.Sheep(self.param, i) for i in range(0, self.sheep_number)]
        [sheeps[i].slow_param(self.param) for i in range(0, slow_num)]

        #shepherdの初期化
        shepherd_in = select_shepherd_model(self.shepherd_model, self.param)

        success_rate = 0

        for trial in range(0, self.trials):
            end_time, success = self.trial_loop_csv(self.file_path_ite_csv.format(slow_num, trial) ,sheeps, shepherd_in)
            success_rate = success_rate + success
            self.write_end_step_csv(self.file_path_tri_csv(trial), end_time, sheeps, shepherd_in)
            [sheeps[i].reset(self.param, i, trial) for i in range(len(sheeps))]
            shepherd_in.reset(self.param)
        
        return success_rate

    def trial_loop_csv(self, file_path, sheeps, shepherd_in):   
        '''
        1trialのループ　csvファイルへの保存
        '''     
        f = open(file_path, mode='a')
        writer = csv.writer(f)
        ###
        success = 0
        for t in range(0, self.n_iter):     
            self.write_line_csv(writer, sheeps, shepherd_in)
            self.update(sheeps, shepherd_in, self.goal)
                
            if self.is_success(sheeps) == True: #誘導が成功すると途中でシミュレーション終了
                success = 1
                break
        ###
        f.close()
        return t, success
    
    def trial_loop_csv_experimental(self, slow_num, trial):
        '''
        1trialのループ　csvファイルへの保存
        '''            
        #sheepsの初期化
        sheeps = [models.sheep.Sheep(self.param, i) for i in range(0, self.sheep_number)]
        [sheeps[i].slow_param(self.param) for i in range(0, slow_num)]
        #初期位置の設定
        [sheeps[i].reset(self.param, i, trial) for i in range(len(sheeps))]

        #shepherdの初期化
        shepherd_in = select_shepherd_model(self.shepherd_model, self.param)

        #csvファイルを開きながらiterationを回す
        f = open(self.file_path_ite_csv.format(slow_num, trial), mode='a')
        writer = csv.writer(f)

        ###
        success = 0
        for t in range(0, self.n_iter):
            self.write_line_csv(writer, sheeps, shepherd_in)
            self.update(sheeps, shepherd_in, self.goal)
                
            if self.is_success(sheeps) == True: #誘導が成功すると途中でシミュレーション終了
                success = 1
                break
        ###
        f.close()

        # 終了時の時刻と羊,牧羊犬の位置を記録(waitが必要だが未実装)
        #with gzshelve.open(self.file_path_tri.format(slow_num)) as db:
        #    self.write_line(db, trial, [t, sheeps, shepherd_in])
        return (slow_num, success)
    
    def write_line_csv(self, writer, sheeps, shepherd):
        '''
        そのstep時の羊, 牧羊犬の位置をcsvファイルに1行追加
        '''
        s = ["k " + str(sheeps[i].position) for i in range(len(sheeps))] 
        #特殊マーカーごとにplotの色を変更
        for d in shepherd.unique_sheep.items(): 
            s[d[1].no] = s[d[1].no].replace('k', d[0]) 

        s.append("r " + str(shepherd.position))
        writer.writerow(s)
    
    def write_end_step_csv(self, file_path, end_step, sheeps, shepherd):
        '''
        1trial終了後, 終了時step, 羊, 牧羊犬の位置をcsvファイルで保存
        '''  
        with open(file_path, mode='a') as f:
            writer = csv.writer(f)
            s = [end_step]
            [s.append(str(sheeps[i].position)) for i in range(len(sheeps))]
            s.append(shepherd.position)
            writer.writerow(s)
