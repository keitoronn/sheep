import os
import csv
import datetime
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio

from .plot_ss import * 

'''
csvファイルから各種グラフ, gifの作成
'''

def end_pos_save(file_path, end_step, sheeps, shepherd):
    '''
    end_pos_modeでファイル保存
    '''
    with open(file_path, mode='a') as f:
        writer = csv.writer(f)
        s = [end_step]
        [s.append(str(sheeps[i].position)) for i in range(len(sheeps))]
        s.append(shepherd.position)
        writer.writerow(s)

def all_pos_save(file_path, sheeps, shepherd):
    '''
    all_pos_modeでファイル追記, 保存
    ''' 
    with open(file_path, mode='a') as f:
        writer = csv.writer(f)

        s = ["k " + str(sheeps[i].position) for i in range(len(sheeps))]
        
        #特殊マーカーごとにplotの色を変更
        for d in shepherd.unique_sheep.items(): 
            s[d[1].no] = s[d[1].no].replace('k', d[0]) 

        s.append("r " + str(shepherd.position))
        writer.writerow(s)

def full_csv(directory_path, slow_num, trials):
    '''
    csvの最終行だけを集めたcsvファイルを生成する
    '''
    with open("{}/data/{}.csv".format(directory_path, slow_num), mode='a') as f:
        for trial in trials:
            file_path = "{}/data/{}t{}.csv".format(directory_path, slow_num, trial)
            time, value = read_last_line(file_path)
            writer = csv.writer(f)
            value.insert(0, time)
            writer.writerow(value)


def count_line(file_path):
    '''
    csvの最後行を返す
    '''
    with open(file_path) as f:
        for line_count, _ in enumerate(f, 1):
            pass
    return line_count

def csv_mod_read_row(path, idx):
    '''
    csvファイルの内idx行の文字列を取り出す
    '''
    with open(path, mode='r') as f:
        reader = csv.reader(f)
        line_count = 0
        while True:
            if line_count == idx:
                break
            f.readline()
            line_count += 1
        return next(reader)
    return None

def read_last_line(file_path):
    '''
    csvの最後行を返す
    '''
    line_count = count_line(file_path)
    return line_count, csv_mod_read_row(file_path, line_count-1)

def str_to_nparray(str):
    '''
    文字列からnp.array形式に変換 
    
    ex. "[0.1, 0.1]" → np.array(0.1, 0.1) 
    '''
    #re_str = str[1:-1].split()
    #l = [float(re_str[i]) for i in range(len(re_str))]
    color = str[0]
    np_str = str[3:-1].split()
    l = [float(np_str[i]) for i in range(len(np_str))]
    return np.array(l)

def str_to_color_nparray(str):
    '''
    文字列からmatplotlibのplotの色とnp.array形式に変換 
    
    ex. "k [0.1, 0.1]" → 'k' np.array(0.1, 0.1) 
    '''
    color = str[0]
    np_str = str[3:-1].split()
    #print("str:{} re:{}".format(str, str[1:-1]))
    l = [float(np_str[i]) for i in range(len(np_str))]
    return  color, np.array(l)

def get_csv_list(directory_path, slow_num, param, success=True):
    '''
    特定のtrialのcsvファイルのtrialリストを返す

    Parameters
    ----------
    success: Bool

        Shepherdingに成功したtrialのlistを取得したい True
    '''
    file_path = directory_path + "/data/" + str(slow_num) + ".csv"
    files = []
    end_steps = []
    with open(file_path, mode='r') as f:
        reader = csv.reader(f, delimiter=',')
        trial = 0
        for row in reader:
            sheeps_pos = [str_to_nparray(str) for str in row[1:-1]]
            successed = int(row[0]) < param["n_iter"] - 1
            if successed:
                files.append(trial)
                end_steps.append(int(row[0]))
            trial = trial + 1
        all_trials = range(0, reader.line_num) 

    #失敗したものだけ取り出したいとき
    if success == False:
        files = list(set(all_trials) ^ set(files))
    return files

def get_end_step_list(directory_path, slow_num, param, successed=False):
    '''
　　成功したtrialのend_stepのリストを返す
    '''
    file_path = directory_path + "/data/" + str(slow_num) + ".csv"
    end_steps = []
    s_end_steps = []
    with open(file_path, mode='r') as f:
        reader = csv.reader(f, delimiter=',')
        trial = 0
        for row in reader:
            sheeps_pos = [str_to_nparray(str) for str in row[1:-1]]
            end_steps.append(int(row[0]))
            
            if int(row[0]) < param["n_iter"] - 1:
                s_end_steps.append(int(row[0]))
            trial = trial + 1
    if successed==True:
        return s_end_steps
    return end_steps

def csv_gif(directory_path, param, slow_num, trial):
    '''
    csvファイルからgifを生成する
    '''
    file_path = directory_path + "/data/" + "{}t{}.csv".format(slow_num, trial) 
    with open(file_path) as f:
        reader = csv.reader(f, delimiter=',')
        
        fig, ax = plt.subplots(figsize=(8,8))
        
        row_num = 0
        for row in reader:
            sheeps_color = []
            sheeps_pos = []
            for i in range(len(row)-1):
                color, pos = str_to_color_nparray(row[i])
                sheeps_color.append(color)
                sheeps_pos.append(pos)
            #sheeps_pos = [str_to_color_nparray(row[i]) for i in range(len(row)-1)]
            shepherd_color, shepherd_pos = str_to_color_nparray(row[-1])
            #ax.set_title(row)
            
            init_plot_line_csv(ax, param, [sheeps_color, sheeps_pos], [shepherd_color, shepherd_pos], slow_num)

            fig_path = directory_path + "/gif/{}t{}/{}.png".format(slow_num, trial, row_num)
            row_num = row_num + 1
            fig.savefig(fig_path) 
            ax.clear()
    generate_gif(directory_path, row_num, slow_num, trial)

def generate_gif(directory_path, row_num, slow_num, trial):
    '''
    アニメーションgifの生成 imageio使用
    '''
    gif_path = directory_path + "/gif/" + "{}t{}.gif".format(slow_num, trial)
    frames_path = directory_path + "/gif/{}t{}/".format(slow_num, trial) + "{i}.png"
    with imageio.get_writer(gif_path, mode='I', fps=60) as writer:
        for i in range(row_num):
            writer.append_data(imageio.imread(frames_path.format(i=i)))
    
def box_plot(slow_nums, directory_path, param):
    """
    end_posモードで保存したcsvファイルから読み込み, ゴールからの距離の箱ひげ図を生成, 保存する
    """
    #n回trial実施したときの箱ひげ図1つ分　slow_num分描画
    maxs = []
    means = []
    goal = np.array(param["goal"])
    for slow_num in slow_nums:
        file_path = directory_path + "/data/" + str(slow_num) + ".csv"
        max = []
        mean = []
        with open(file_path) as f:
            reader = csv.reader(f, delimiter=',')
 
            l_f = []
            #1行ずつrowで取得
            for row in reader:
                sheeps_pos = [str_to_nparray(str) for str in row[1:-1]]
                #print(sheeps_pos)
                #30匹のゴールからの最大値を追加
                max.append(max_distance(sheeps_pos, goal))
                mean.append(mean_distance(sheeps_pos, goal))
        maxs.append(max)
        means.append(mean)

    #最大値, 平均値のbox_plotを保存
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

def patch_plot(slow_nums, directory_path, param, grid=[2,5]):
    """
    end_posモードで保存したcsvファイルから読み込み,

    失敗したtrialを最大10枚抜き出して散布図で表示
    """
    for slow_num in slow_nums:
        file_path = directory_path + "/data/" + str(slow_num) + ".csv"
        trial_list = get_csv_list(directory_path, slow_num, param, success=False)
        fig = plt.figure(figsize=(20,10))
        
        #グラフの数
        graph_number = grid[0] * grid[1] 
        #取り出したtrialの数がグラフの数より少ない場合, そのtrialの数だけのグラフを出力する
        if len(trial_list) <= graph_number:
            graph_number = len(trial_list)

        for i in range(0, graph_number):
            pos = []
            row = csv_mod_read_row(file_path, trial_list[i])
            sheeps = list(map(str_to_color_nparray, row[1:-1])) 
            shepherd_color, shepherd_pos = str_to_color_nparray(row[-1])

            ax = fig.add_subplot(grid[0], grid[1], i+1)
            init_plot_line_csv(ax, param, sheeps, [shepherd_color, shepherd_pos], slow_num)
        
        fig.tight_layout()
        fig_path = directory_path + "/graph/patch_plot/" + str(slow_num) + ".png"
        fig.savefig(fig_path) 

def bar_plot(slow_nums, result, directory_path):
    '''
    誘導成功率を棒グラフで表示, 保存
    '''
    fig, ax = plt.subplots(figsize=(8,8))
    ax.plot(slow_nums, result)

    for x, y in zip(slow_nums, result):
        ax.text(x, y, y, ha='center', va='bottom')
    ax.set_xlabel('slow sheep rate')  # x軸ラベル
    ax.set_ylabel('success rate')  # y軸ラベル
    ax.set_title('success rate')  # グラフタイトル
    ax.set_xlim(0, len(slow_nums) + 1)
    ax.set_ylim(-5, 105)
    fig_path = directory_path + "/graph/success_rate.png"
    fig.savefig(fig_path)
    
def success_time_plot(slow_nums, directory_path, param):
    '''
    成功したtrialの最小, 最大, 平均step数を箱ひげ図で表示, 保存
    '''
    fig, ax = plt.subplots(figsize=(8,8))
    sx_times = []
    for slow in slow_nums:
        list = get_end_step_list(directory_path, slow, param, successed=True)
        sx_times.append(list)
    fig, ax = box_sub_plot(sx_times, slow_nums)
    ax.set_xlabel('slow sheep rate')  # x軸ラベル
    ax.set_ylabel('success time')  # y軸ラベル
    ax.set_title('success time')  # グラフタイトル
    fig_path = "{}/graph/{}.png".format(directory_path, "success_time") 
    fig.savefig(fig_path)

def max_distance(sheeps, goal):
    '''
    羊30匹のうちゴールからの最大の距離を求める
    '''
    max = 0
    max_sheep = 0
    for i in range(len(sheeps)):
        d =  np.linalg.norm(sheeps[i] - goal)
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
        d =  np.linalg.norm(sheeps[i] - goal)
        d_all = d_all + d
    mean = d_all/len(sheeps)
    return mean
