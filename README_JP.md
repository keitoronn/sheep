
# Sheep Shepherding Program 
Sheep Shepherding Program for 2021 bachelor thesis

# Features

* デモモード

  matplotlibのアニメーションでシミュレーションの状況を見ることができます.
* ノーマルモード
  
  パラメータを設定して, マルチプロセスで多くの試行回数実行することができます.

# Requirement
 
* Python 3.6.5 or higher
 
Linux Ubuntu 環境のみテスト済み
 
# Installation

pip コマンドで必要なパッケージをインストールしてください.
 
```bash
pip3 install -r requirement.txt
```

# Docker 
dockerイメージの作成
```bash
docker-compose build
```
dockerコンテナの立ち上げ
```bash
docker-compose up -d
```
dockerコンテナに入る
```bash
docker-compose exec python3 bash
```
 
# Usage
 
-h オプションで使い方のヘルプが出ます.

```bash
python3 main.py -h
```
 
## Demo 
注意：この機能はGUI環境でのみ使用可能です.
デモモードはこのコマンドを使ってください. 
 
アニメーションでシミュレーションの様子をチェックできます.
```bash
python3 main.py -d
```

## Set Config File
コンフィグファイルを使用して, パラメータを設定することができます.

例えば, "config/test.json"を設定したいなら以下のコマンドを使ってください.

注意:パラメータによってはプログラムの実行に長時間（10時間以上）かかります. 計算機サーバの使用を推奨します.
```bash
python3 main.py -p "config/test.json"
```

## Config File
コンフィグファイルは自分で自由に設定することができます.

書式など詳細は [ここ](docs/config_file_format.md) を参照してください. 以下は一例です.

``` json:config/demo.json
{
    "shepherd_model": "farthest_agent",
    "process_number": 1,
    "trial_number": 1,
    "sheep_number": 20,
    "slow_sheep_number": [10, 10],
    "n_iter": 200,
    "goal": [50,50],
    "goal_radius": 15,
    "shepherd_initial_pos": [-30,-50],
    "sheep_initial_pos_radius": 90,
    "sheep_initial_pos_base":[0,0],
    "sheep_param": [100.0, 0.5, 2.0, 500.0],
    "slow_sheep_param": [100.0, 0.5, 2.0, 0.0],
    "shepherd_param": [10.0, 200, 4.0]
}
```

## Log File
-pオプションで, パラメータを設定するとログが生成されます. 

ログファイルの中身は全時刻での全ての羊と牧羊犬の位置です.

-cオプションで, ファイルの形式をcsv形式に設定できます. デフォルトはshelve形式です.

shelve形式の詳細は [Python Document of shelve format](https://docs.python.org/ja/3/library/shelve.html)を参照してください. 
  

### 注意: shelve形式の場合, シミュレーション時間によってはファイル容量が膨大になる可能性があります. ファイル容量の節約のためcsv形式を使った方が良いかもしれません. また, shelveファイルの中身は直接見ることができまんが, ファイル内容に関するコーディングが簡単という利点があります.

ログファイルのパスは "log/yyyy_mmdd_hhmmss/data/". ディレクトリ構造は以下の通り. 
```
log
├── yyyy_mmdd_hhmmss
│   ├── data
│   ├── gif
│   ├── graph
│   │   ├── distance_max.png
│   │   ├── distance_mean.png
│   │   ├── patch_plot
│   │   └── success_time.png
│   ├── result.csv
│   └── setting.json
```

## Graph
成功率は"log/yyyy_mmdd_hhmmss/result.csv"に記録してあります.
シミュレーション結果をグラフで見ることができます. パスは "log/yyyy_mmdd_hhmmss/graph/".

グラフの種類

 グラフの名前     |  説明
---- | ----
 distance_max   | 箱ひげ図. シミュレーション終了時のすべての羊のゴールからの距離の最大値
 distance_mean  | 箱ひげ図. シミュレーション終了時のすべての羊のゴールからの距離の平均
 success_time   | 箱ひげ図. 成功時にかかった時間
 patch_plot     | 散布図. 失敗時にシミュレーション終了時の全ての羊の位置.

## Additional Graph
従来法と提案法を比較するグラフを作成するためにgraph.pyを実行します. 以下に示すそれぞれの関数をソースコードで変更しながら使用してください.

```bash
python3 graph.py
```
* gen_graph_n()
   
  Nに関して分類した成功率に関する折れ線グラフ
* gen_graph_rho()

  ρに関して分類した成功率関する折れ線グラフ
* success_time_plot_compare()

  実行ステップ数の比較関するカラー散布グラフ
  

## GIF
シミュレーションのgifファイルを出力したいときはgif.pyを使用してください.
gifファイルの出力先は"log/yyyy_mmdd_hhmmss/gif/".
```bash
python3 gif.py [directory path]
```

詳しくは使い方のヘルプを見てください.
```bash
python3 gif.py -h
```

# Dependencies
* numpy
* matplotlib
* imageio
 
# Note
 
Windows と Mac環境は試していません. 
 
# License
 
"Sheep-Shepherding Program" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
 
 