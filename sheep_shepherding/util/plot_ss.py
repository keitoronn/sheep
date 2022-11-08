import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as anim
import time

'''
Sheep-Shepherding(略してss)の描画 
'''

def init_figure():
    '''
    figureの初期化 
    '''
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    return fig, ax

def init_plot_line(ax, param, sheeps, shepherd):
    '''
    axの初期化 
    '''
    #羊
    for i in range(len(sheeps)):
        if sheeps[i].slow:
            ax.plot(sheeps[i].position[0], sheeps[i].position[1], "k^", alpha=0.5)
        else:
            ax.plot(sheeps[i].position[0], sheeps[i].position[1], "ko", alpha=0.5)
    ax.plot(shepherd.position[0], shepherd.position[1], "ro", alpha=0.5)

    #ゴール地点
    #goal_zone = patches.Circle(param["goal"], param["goal_radius"], ec="k", fc='white', linestyle="dotted", alpha=1)
    goal_zone = patches.Circle(param["goal"], param["goal_radius"], ec="k", fc='white', alpha=1)

    ax.add_patch(goal_zone)
    #x,y軸の範囲
    xy_range = param["sheep_initial_pos_radius"] + 50
    #xy_range = 70
    ax.set_xlim(-xy_range, xy_range)
    ax.set_ylim(-xy_range, xy_range)
    ax.set_aspect('equal')
    

def init_plot_line_csv(ax, param, sheeps, shepherd, slow_num):
    '''
    axの初期化 
    '''
    
    #羊
    for i in range(len(sheeps)):
        sheep_color = sheeps[i][0]     
        sheep_pos = sheeps[i][1]
        if i < slow_num:
            ax.plot(sheep_pos[0], sheep_pos[1], sheep_color + '^', alpha=0.5) 
        else: 
            ax.plot(sheep_pos[0], sheep_pos[1], sheep_color + 'o', alpha=0.5) 
    #牧羊犬
    
    shepherd_color = shepherd[0]
    shepherd_pos = shepherd[1]
    ax.plot(shepherd_pos[0], shepherd_pos[1], shepherd_color + 'o', alpha=0.5)

    #ゴール地点
    goal_zone = patches.Circle(param["goal"], param["goal_radius"], ec="k", fc='white', alpha=1)
    ax.add_patch(goal_zone)

    #x,y軸の範囲
    xy_range = param["sheep_initial_pos_radius"] + 50
    ax.set_xlim(-xy_range, xy_range)
    ax.set_ylim(-xy_range, xy_range)
    ax.set_aspect('equal') 

def plot_per_iteration(axes, current_step, sheeps, shepherd, animation=False):
    '''
    1stepごとの描画
    '''
    #text.set_text("t={}".format(t)) 
    plt.title("t={}".format(current_step))

    #全てのsheep, shepherdのLine2D要素を取り出す
    lines = plt.gca().get_lines()

    for i in range(len(sheeps)):
        line = lines[i]
        line.set_data(sheeps[i].position[0], sheeps[i].position[1])
        line.set_color("0.3")
        if sheeps[i].slow:
            line.set_marker("^") 
        else:
            line.set_marker("o") 
    lines[-1].set_data(shepherd.position[0], shepherd.position[1])

    #特殊マーカーごとにplot
    for d in shepherd.unique_sheep.items():           
        lines[d[1].no].set_color(d[0]) 
    
    #アニメーションの場合
    if animation == True:
        plt.pause(0.01)