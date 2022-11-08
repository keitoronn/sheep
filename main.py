import os
import time
import datetime
import argparse 
import csv
from multiprocessing import Pool
from itertools import starmap

import sheep_shepherding as ss
from sheep_shepherding.util import analyze
from sheep_shepherding.util import analyze_shelve
from sheep_shepherding.util import config
from sheep_shepherding.util import disk_info

'''
Sheep Shepherding Program for 2021 bachelor thesis
'''

def demo(param, directory_path):
    '''
    デモ用 plotをリアルタイムで表示, ログは保存しない
    '''
    do = ss.trial.Trial(param, directory_path)
    slow_sheeps = list(range(param["slow_sheep_number"][0], param["slow_sheep_number"][1] + 1))
    values = [(slow_sheeps[0], 10)]
    
    start = time.time() 
    with Pool(processes=param["process_number"]) as pool:
        result = pool.starmap(do.demo, values)
    elapsed_time = time.time() - start
    
    # gifの生成
    png_path = directory_path + "/png"
    analyze_shelve.generate_gif(png_path, directory_path + "/demo.gif", result[0][0])

    return elapsed_time

def multiprocess(param, directory_path, csv_mode=False):
    '''
    サーバー用 マルチプロセスで実行, シミュレーションをすべて再現できるログを保存
    '''
    slow_sheeps = range(param["slow_sheep_number"][0], param["slow_sheep_number"][1] + 1)
    do = ss.trial.Trial(param, directory_path)
    success_rates = []
    
    start = time.time()
    ### 
    with Pool(processes=param["process_number"]) as pool:
        if csv_mode == True:
            success_rates = pool.map(do.loop_csv, slow_sheeps)
        else:
            success_rates = pool.map(do.loop, slow_sheeps)
    ###
    elapsed_time = time.time() - start
    
    #その他各種グラフの生成
    print(csv_mode)
    gen_graph(csv_mode, slow_sheeps, directory_path, param, success_rates)
    return elapsed_time, success_rates   

def multiprocess_experimental(param, directory_path, csv_mode=False):
    '''
    サーバー用 マルチプロセスで実行, シミュレーションをすべて再現できるログを保存

    1trialをpoolに流し込む
    '''
    slow_sheeps = range(param["slow_sheep_number"][0], param["slow_sheep_number"][1] + 1)
    all_trials = range(param["trial_number"])
    
    do = ss.trial.Trial(param, directory_path) 
    values = [(slow_num, trial) for slow_num in slow_sheeps for trial in all_trials]
    
    start = time.time()
    ###
    with Pool(processes=param["process_number"]) as pool:
        if csv_mode == True:
            result_unit = pool.starmap(do.trial_loop_csv_experimental, values)
            [analyze.full_csv(directory_path, slow_num, all_trials) for slow_num in slow_sheeps]
        else:
            result_unit = pool.starmap(do.trial_loop_experimental, values)
            [analyze_shelve.full_db(directory_path, slow_num, all_trials) for slow_num in slow_sheeps]
    ###
    elapsed_time = time.time() - start

    success_rates = [0] * len(slow_sheeps)
    for i in range(len(result_unit)):
        success_rates[result_unit[i][0] - param["slow_sheep_number"][0]] = success_rates[result_unit[i][0] - param["slow_sheep_number"][0]] + result_unit[i][1] 
    
    #その他各種グラフの生成
    gen_graph(csv_mode, slow_sheeps, directory_path, param, success_rates)
    return elapsed_time, success_rates

def gen_graph(csv_mode, slow_sheeps, directory_path, param, success_rates):
    '''
    各種グラフの生成, 保存
    '''
    write_success_rates_csv(directory_path + "/result.csv", success_rates)
    #analyze.box_plot(slow_sheeps, directory_path, param) 

    #グラフの保存
    if csv_mode == True:
        analyze.box_plot(slow_sheeps, directory_path, param) 
        analyze.success_time_plot(slow_sheeps, directory_path, param)
        analyze.patch_plot(slow_sheeps, directory_path, param)
    else:
        analyze_shelve.box_plot(slow_sheeps, directory_path, param) 
        analyze_shelve.success_time_plot(slow_sheeps, directory_path, param)
        analyze_shelve.patch_plot(slow_sheeps, directory_path, param)
        
def write_success_rates_csv(file_path, s):
    '''
    csv形式で成功率の出力 
    
    後でexcelのグラフを作りやすくするため
    '''
    with open(file_path, mode='a') as f:
        writer = csv.writer(f)
        writer.writerow(s)

def make_dir():
    '''
    現在時刻でログ用のディレクトリを作成 

    形式: yyyy_MMdd_HHMMSS
    ''' 
    now = datetime.datetime.now()
    now_string = now.strftime('%Y_%m%d_%H%M%S')  # yyyy_MMdd_HHMMSS形式
    directory_path = "log/{}".format(now_string)
    graph_path = "log/{}/graph/patch_plot".format(now_string)
    data_path = "log/{}/data".format(now_string)
    gif_path = "log/{}/gif".format(now_string)

    os.makedirs(graph_path) 
    os.makedirs(data_path)
    os.makedirs(gif_path)
    return os.path.abspath(directory_path)

def get_param(param_file_path):
    '''
    パラメータの取得 パラメータはdict形式
    '''
    param = config.load(param_file_path)
    return param

def arg_parse():
    '''
    コマンドライン引数の設定, 取得
    '''
    parser = argparse.ArgumentParser(description="Sheep Shepherding Program for 2021 bachelor thesis")
    parser.add_argument('-d', '--demo', action='store_true', help='execute in demo mode')
    parser.add_argument('-c', '--csv', action='store_true', help='save log file in csv format')
    parser.add_argument('-p', '--param_file_path', default="./config/demo.json", help='parameter file path')
    
    return parser.parse_args()

if __name__ == '__main__':
    #メイン関数
    args = arg_parse()
    param = get_param(args.param_file_path)
    dir_path = None
    
    if args.demo == True:    
        dir_path = 'demo'
        elapsed_time = demo(param, dir_path)
    else:
        dir_path = make_dir()

        #elapsed_time, success_rates = multiprocess(param, dir_path, csv_mode=args.csv)
        elapsed_time, success_rates = multiprocess_experimental(param, dir_path, csv_mode=args.csv)

        param_file_basename =  os.path.splitext(os.path.basename(args.param_file_path))[0]
        success_rates.insert(0, param_file_basename)
        #paramファイルの名前と成功率を書いたcsvファイルを出力
        write_success_rates_csv("results.csv", success_rates)
            
    str = "{}, {}, {}".format(dir_path, datetime.timedelta(seconds=int(elapsed_time)), args.param_file_path)
    print(str)
    
    #paramファイルのコピーを作成
    config.write_reshaped(dir_path + "/setting.json", param)

    #ディスク使用容量のwarningを出す
    disk_info.warn_directory_size(dir_path)
    disk_info.warn_disk_usage(limit_percentage=80)