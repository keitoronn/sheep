import json
import os
import re

'''
configファイルの読み込み
'''

def load(json_path, complement=True):
    '''
    jsonファイルを読み込む 
    
    dict形式で読み込んだデータを返す
    '''
    json_dict = None
    with open(json_path, 'r') as f:
        json_dict = json.load(f)   

    if complement == True:
        json_dict = complement_dict(json_dict)
    #print(json_dict)
    return json_dict

def complement_dict(json_dict):
    '''
    足りないkeyをdefault.jsonに記載されているvalueで補完する
    '''
    with open("./config/default.json", 'r') as f:
        default_dict = json.load(f)

    for k in default_dict.keys():
        if k not in json_dict:
            json_dict[k] = default_dict[k]

    return json_dict

def write(json_path, dict):
    '''
    dict形式のデータをファイル出力
    '''
    with open(json_path, 'w') as f:
        json.dump(dict, f)
    
def write_reshaped(json_path, dict):
    '''
    dict形式のデータで整形したものをファイル出力
    '''
    with open(json_path, 'w') as f:
        dump_data = json.dumps(dict, indent=4)
        #'['と']'で囲まれた部分では改行をなくす
        re_dump_data = re.sub('\[(.*?)\]',dashrepl, dump_data, flags=re.DOTALL)
        f.write(re_dump_data)

def dashrepl(matchobj):
    #print(matchobj)
    return matchobj.group(0).replace("\n", "").replace(" ", "")

def diff_from_defalut(self, defalut_params, params):
    '''
    defalut.jsonと異なるキーのみを取り出す
    '''
    diff_list = []
    for k in params.keys():
        if defalut_params[k] != params[k]:
            diff_list.append("{}:{}".format(k, params[k]))
    return diff_list