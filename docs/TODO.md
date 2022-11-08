# TODO:
# all
- [x] パラメータを一括で変更できるconfigファイルを作りたい
- [x] パッケージ化
- [ ] docker環境の整備
# docs
- [x] README.mdの作成
# analyze.py
- [x] 成功したときの最小 平均　最大 step数のグラフ
- [x] csvファイルからgif作成機能
- [x] csvファイルからgifを生成するときにplotの色を時刻によって変化できる仕組み
# analyze_shelve.py
- [x] 保存方式をcsv形式からpickle形式に変更
- [x] pickleファイルから各種グラフの作成
- [x] pickleファイルからgif作成機能
- [x] pickleファイルからgifを生成するときにplotの色を時刻によって変化できる仕組み
# sheep.py
- [x] sheeps初期配置のrandomのseed固定
# collective_shepherd.py 
- [ ] slow_sheepの数が0/30のときでも実行できるように
# gif.py
- [x] 全てのtrialの中から30個ほど取り出して生成する
- [ ] gifを横に並べて一度に見れるようにする
# plot.py -> plot_ss.py
- [x] demoモードだけでなくlogからpatch_plotやgif作成時にも統一的に使えるように全面的に修正
- [ ] 羊の初期配置に応じたplotのx,y範囲の変更
# trial.py
- [x] csv形式での保存とpickle形式での保存で共通して使えるようにする(メソッドは別)
- [ ] trialのindexのみ指定して実行できるように
# gzshelve.py
- [x] 圧縮機能付きの改変shelveライブラリの実装
# disk_info.py
- [x] フォルダの容量の表示
- [x] ディスクの利用可能容量の表示
- [x] フォルダ容量が一定容量を超えた場合の警告機能
- [x] ディスクの使用率が一定割合を超えた場合の警告機能