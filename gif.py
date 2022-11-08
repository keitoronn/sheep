import os
import random
import datetime
import numpy as np
import argparse

from multiprocessing import Pool
from sheep_shepherding.util import config
from sheep_shepherding.models import select_shepherd_model
from sheep_shepherding.util import analyze_shelve

'''
gifの複数生成　計算機サーバ推奨
'''

def get_random_paths(directory_path, number=30, all=False, success=False):
    '''
    全トライアル中, ランダムに誘導失敗したものをいくつか取ってくる

    Parameters
    ----------
    number: int 

    取り出すファイルパスの最大数

    all: Bool

    Trueならすべてのslow_numについて(1つのslow_numについて3つまで)ファイルパスを取り出す

    success : Bool

    成功したtrialを取り出すか, 失敗したtrialを取り出すか
    '''
    
    param = config.load(directory_path + "/setting.json")
    
    file_paths = []
    #1つのslow_numについて取ってくるtrialの最大数は3とする（とりあえず）
    for i in range(1, param["slow_sheep_number"][1]):
        l = analyze_shelve.get_db_path_list(directory_path, i, param, success=success)
        if len(l) > 3:
            l = l[:3]
        file_paths.extend(l)

    #number個randomに抽出
    if all == False:
        file_paths = random.sample(file_paths, number)

    return file_paths

def generate_gifs(directory_path, success=False):
    '''
    全trialの中から複数のgifを生成する gifの最大生成数は指定しない（指定はできる）
    '''
    param = config.load(directory_path + "/setting.json")
    db_paths = get_random_paths(directory_path, all=True, success=success)
    gif_dir = directory_path + "/gif"

    p = Pool(processes=param["process_number"])
    values = [(db_path, gif_dir, param) for db_path in db_paths]
    
    p.map(arg_wrapper, values)   
    p.close()
    return

def generate_gifs_slow_sheep(directory_path, slow_num, success=False):
    '''
    全trialの中から, 特定のslow_numについて複数のgifを生成する　gifの最大生成数は"process_number"
    '''
    param = config.load(directory_path + "/setting.json")
    db_paths = analyze_shelve.get_db_path_list(directory_path, slow_num, param, success)

    #gifの最大生成数をとりあえずprocess数にする
    gif_number = param["process_number"]
    if len(db_paths) > gif_number:
        db_paths = db_paths[:gif_number]

    gif_dir = directory_path + "/gif"

    p = Pool(processes=param["process_number"])
    values = [(db_path, gif_dir, param) for db_path in db_paths]
    p.map(arg_wrapper, values)    
    p.close()
    return

def arg_wrapper(args):
    analyze_shelve.db_gif(*args)
    return

def arg_parse():
    '''
    コマンドライン引数の設定, 取得
    '''
    parser = argparse.ArgumentParser(description="gif generator for sheep shepherding trial")
    parser.add_argument('directory_path', help='log directory path') #必須引数
    parser.add_argument('-n', '--number', help='set number of slow sheep')
    parser.add_argument('-s', '--success', action='store_true', help='generate gif of similation when navigation succeeded')
    
    return parser.parse_args()

if __name__ == '__main__':
    args = arg_parse()

    if args.number == None:
        generate_gifs(args.directory_path, args.success)
    else: 
        generate_gifs_slow_sheep(args.directory_path, args.number, args.success)