import os
import shutil
import datetime
import imageio
import numpy as np

import matplotlib.pyplot as plt
from .. import gzshelve
from .plot_ss import * 

'''
shelveファイルから各種グラフ, gifの作成
shelveはpickleのデータベース実装なのでkeyは文字列でしか指定できない
'''
def print_line(db, key):
    print(db[str(key)])

def read_line(db, key):
    return db[str(key)]

def write_line(db, key, value):
    db[str(key)] = value
    
def get_line_num(db):
    return len(db.keys())

def full_db(directory_path, slow_num, trials):
    '''
    dbの最終行だけを集めたdbファイルを生成する
    '''
    with gzshelve.open("{}/data/{}.db".format(directory_path, slow_num)) as db:
        for trial in trials:
            file_path = "{}/data/{}t{}.db".format(directory_path, slow_num, trial)
            time, value = read_last_line(file_path)
            db[str(trial)] = [time, value[0], value[1]]

def read_last_line(file_path):
    '''
    dbの最後行を返す
    '''
    with gzshelve.open(file_path, flag='r') as db:
        return len(db.keys())-1, db[str(len(db.keys()) - 1)]

def get_db_path_list(directory_path, slow_num, param, success=True):
    '''
    特定のtrialのdbファイルパスのリストを返す

    Parameters
    ----------
    success: Bool

        Shepherdingに成功したtrialのリストを取得したい True
    '''
    file_path = "{}/data/{}.db".format(directory_path, slow_num)
    all_file_paths = []
    file_paths = []
    end_steps = []
    print(file_path)
    with gzshelve.open(file_path, flag='r') as db:
        for i in range(get_line_num(db)):
            l = read_line(db, i)
            end_step = l[0]
            all_file_paths.append("{}/data/{}t{}.db".format(directory_path, slow_num, i))
            
            if end_step < param["n_iter"] - 1:
                file_paths.append("{}/data/{}t{}.db".format(directory_path, slow_num, i))

    #失敗したものだけ取り出したいとき
    if success == False:
        file_paths = list(set(all_file_paths) ^ set(file_paths)) #元のリストの順番は保証されない

    return file_paths

def get_db_list(directory_path, slow_num, param, success=True):
    '''
    特定のtrialのdbファイルのtrialリストを返す

    Parameters
    ----------
    success: Bool

        Shepherdingに成功したtrialのリストを取得したい True
    '''
    all_trials = range(0, param["trial_number"])
    specific_trials = []
    end_steps = []

    file_path = "{}/data/{}.db".format(directory_path, slow_num)
    with gzshelve.open(file_path, flag='r') as db:
        for i in range(get_line_num(db)):
            l = read_line(db, i)
            end_step = l[0]

            if end_step < param["n_iter"] - 1:
                specific_trials.append(i)
                end_steps.append(end_step)

    #失敗したものだけ取り出したいとき
    if success == False:
        specific_trials = list(set(all_trials) ^ set(specific_trials)) #元のリストの順番は保証されない

    return specific_trials, end_steps

def db_gif(db_path, gif_directory, param):
    '''
    dbファイルからgifの作成

    Parameters
    ----------
    db_path: string

        生成元のdbファイルのパス
    
    gif_directory

        gifを生成するディレクトリ (gifファイル名は指定しなくてよい)
    '''
    # slow_num, trialの数字を取り出す
    db_file_name = os.path.splitext(os.path.basename(db_path))[0]
    print(db_file_name)

    db = gzshelve.open(db_path, flag='r')
    l = read_line(db, 0)
    
    fig, ax = init_figure()
    init_plot_line(ax, param, sheeps=l[0], shepherd=l[1])

    # gif作成時の作業ディレクトリ（pngファイルの一時置き場所）の作成
    png_path = gif_directory + '/' + db_file_name
    os.makedirs(png_path) 
    all_line = get_line_num(db)

    for line in range(all_line):
        l = read_line(db, line)
        plot_per_iteration(ax, line, sheeps=l[0], shepherd=l[1])
        fig.savefig(png_path + "/{}.png".format(line))
    db.close()

    gif_path = gif_directory + "/{}.gif".format(db_file_name)
    generate_gif(png_path, gif_path, all_line)
    #作業ディレクトリの削除
    shutil.rmtree(png_path)

def generate_gif(png_path, gif_file_path, frame):
    '''
    アニメーションgifの生成 imageio使用
    '''
    frames_path = png_path + "/{i}.png"
    with imageio.get_writer(gif_file_path, mode='I', fps=60) as writer:
        for i in range(frame):
            writer.append_data(imageio.imread(frames_path.format(i=i)))

def patch_plot_wrapper(args):
    patch_plot(*args)
    return

def patch_plot(slow_nums, directory_path, param, grid=[2,5]):
    '''
    end_posモードで保存したcsvファイルから読み込み,

    失敗したtrialを最大10枚抜き出して散布図で表示
    '''
    for slow_num in slow_nums:
        db_path = "{}/data/{}.db".format(directory_path, slow_num)
        trial_list, end_step_list = get_db_list(directory_path, slow_num, param, success=False)

        fig = plt.figure(figsize=(20,10))
        
        #グラフの数
        graph_number = grid[0] * grid[1] 
        #取り出したtrialの数がグラフの数より少ない場合, そのtrialの数だけのグラフを出力する
        if len(trial_list) <= graph_number:
            graph_number = len(trial_list)

        for i in range(0, graph_number):
            with gzshelve.open(db_path, flag='r') as db:
                l = read_line(db, trial_list[i])
                ax = fig.add_subplot(grid[0], grid[1], i+1)
                ax = init_plot_line(ax, param, l[1], l[2])
            
        fig.tight_layout()
        fig_path = "{}/graph/patch_plot/{}.png".format(directory_path, slow_num)
        fig.savefig(fig_path)

def line_plot(slow_nums, result, directory_path):
    '''
    誘導成功率を折れ線グラフで表示, 保存
    '''
    fig, ax = plt.subplots(figsize=(8,8))
    ax.plot(slow_nums, result)

    ax.set_xlabel('slow sheep rate')  # x軸ラベル
    ax.set_ylabel('success rate')  # y軸ラベル
    ax.set_title('success rate')  # グラフタイトル

    ax.set_xlim(0, len(slow_nums) + 1)
    ax.set_ylim(-5, 105)
    fig_path = directory_path + "/graph/successs_rate.png"
    fig.savefig(fig_path)
    
def success_time_plot(slow_nums, directory_path, param):
    '''
    成功したtrialの最小, 最大, 平均step数を箱ひげ図で表示, 保存
    '''
    sx_times = []
    for slow in slow_nums:
        trial_list, end_step_list = get_db_list(directory_path, slow, param)
        sx_times.append(end_step_list)
    
    fig, ax = box_sub_plot(sx_times, slow_nums)  

    ax.set_xlabel('slow sheep rate')  # x軸ラベル
    ax.set_ylabel('sucess time')  # y軸ラベル
    ax.set_title('success time')  # グラフタイトル
    fig_path = "{}/graph/{}.png".format(directory_path, "success_time") 
    fig.savefig(fig_path)

def box_plot(slow_nums, directory_path, param):
    '''
    dbファイルから読み込み, 終了時stepにおけるゴールからの距離の箱ひげ図を生成, 保存する
    '''
    #n回trial実施したときの箱ひげ図1つ分　slow_num分描画
    maxs = []
    means = []
    goal = np.array(param["goal"])
    for slow_num in slow_nums:
        db_path = "{}/data/{}.db".format(directory_path, slow_num)
         
        max = []
        mean = []
        with gzshelve.open(db_path) as db:
            line_num = get_line_num(db)
        
            for i in range(0, line_num):
                l = read_line(db, i)
                
                max.append(max_distance(l[1], goal))
                mean.append(mean_distance(l[1], goal))

        maxs.append(max)
        means.append(mean)

    fig, ax = box_sub_plot(maxs, slow_nums)
    ax.set_xlabel('slow sheep rate')  # x軸ラベル
    ax.set_ylabel('max of sheep distance from goal')  # y軸ラベル
    ax.set_title('max of sheep distance from goal')  # グラフタイトル
    fig_path = "{}/graph/{}.png".format(directory_path, "distance_max") 
    fig.savefig(fig_path)

    fig, ax = box_sub_plot(means, slow_nums)
    ax.set_xlabel('slow sheep rate')  # x軸ラベル
    ax.set_ylabel('mean of sheep distance from goal')  # y軸ラベル
    ax.set_title('mean of sheep distance from goal')  # グラフタイトル
    fig_path = "{}/graph/{}.png".format(directory_path, "distance_mean") 
    fig.savefig(fig_path)

def box_sub_plot(plot_list, slow_nums):
    '''
    box_plotの描画部分
    '''
    fig, ax = plt.subplots(figsize=(8,8))
    #外れ値表示なしでboxplotを描画
    bp = ax.boxplot(plot_list, whis=[0,100], showmeans=True)
    ax.set_xticklabels(slow_nums)
    plt.grid()

    return fig, ax

def max_distance(sheeps, goal):
    '''
    羊30匹のうちゴールからの最大の距離を求める
    '''
    max = 0
    max_sheep = 0
    for i in range(len(sheeps)):
        d =  np.linalg.norm(sheeps[i].position - goal)
        if d > max:
            max = d
    return max

def mean_distance(sheeps, goal):
    '''
    羊30匹のゴールからの距離の平均を求める
    '''
    mean = 0
    d_all = 0
    for i in range(len(sheeps)):
        d =  np.linalg.norm(sheeps[i].position - goal)
        d_all = d_all + d
    mean = d_all/len(sheeps)
    return mean

def sheep_distance(sheeps):
    '''
    羊同士の距離の平均 羊同士の距離はそれぞれ一番近い羊を用いる
    '''
    distance_list = []
    for i in range(len(sheeps)):
        l = []
        for j in range(len(sheeps)):
            if i!= j:
                d = np.linalg.norm(sheeps[i].position - sheeps[j].position)
                l.append(d)
        min_distance = min(l)
        distance_list.append(min_distance)
    
    ave = sum(distance_list) / len(distance_list)
    return ave