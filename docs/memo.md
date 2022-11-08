# マークダウン記法
- [マークダウン記法 一覧表・チートシート - Qiita](https://qiita.com/kamorits/items/6f342da395ad57468ae3#%E3%83%9E%E3%83%BC%E3%82%AF%E3%83%80%E3%82%A6%E3%83%B3%E3%81%AE%E3%82%A8%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%97)

# パッケージ化
##  \_\_init\_\_.pyの役割
\_\_init\_\_.pyはそもそもなくてもいけるらしい. （python3.3以上の名前空間パッケージという機能にあたるらしい)
\_\_init\_\_.pyの書き方はGPyOptとPandasを参考にした.

(参考)
- [5. インポートシステム — Python 3.9.1 ドキュメント](https://docs.python.org/ja/3/reference/import.html)
- [ - パッケージとモジュール - とほほのPython入門](http://www.tohoho-web.com/python/module.html)
- [Pythonパッケージは、本を目で追うだけではわかりにくい。 | Snow Tree in June](https://snowtree-injune.com/2018/09/04/package1/)
- [\_\_init\_\_.pyの役割とは？パッケージ化やimportの関係は？ | スタートアップIT企業社長のブログ](https://shimi-dai.com/python-what-is-__init__-py/)
- [SheffieldML/GPyOpt · GitHub](https://github.com/SheffieldML/GPyOpt/tree/master/GPyOpt)
- [pandas-dev/pandas · GitHub](https://github.com/pandas-dev/pandas/tree/master/pandas)

# main.py
## CPU並列計算の方法
multiprocessing.Poolを使う. 複数の引数を取る場合はPool.starmapかwrapper経由で使用する.

(参考)
- [pythonで並列化入門 (multiprocessing.Pool) - Qiita](https://qiita.com/studio_haneya/items/1cf192a0185e12c7559b)
- [Pythonの並列処理・並行処理をしっかり調べてみた - Qiita](https://qiita.com/simonritchie/items/1ce3914eb5444d2157ac#concurrentfuture%E4%B8%A6%E8%A1%8C%E5%87%A6%E7%90%86%E3%81%AE%E3%82%B3%E3%83%BC%E3%83%89%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB)
- [【python】mapで複数の引数を渡したいときはstarmapが便利 - 静かなる名辞](https://www.haya-programming.com/entry/2018/04/21/171008)

## コマンドライン引数を使用する(ArgumentParser)
コマンドライン引数を利用するためにはArgumentParserを利用する. -hオプションで指定したときに出る記述もきちんとしておこう.

(参考)
- [ArgumentParserの使い方を簡単にまとめた - Qiita](https://qiita.com/kzkadc/items/e4fc7bc9c003de1eb6d0#%E5%BF%85%E9%A0%88%E5%BC%95%E6%95%B0)

# analyze.py
## boxplotで外れ値が表示される

boxplotのオプションwhisで変更できる
```
plt.boxplot(x, whis="range")
```
(参考)
- [[matplotlib] 51. 箱ひげ図(plt.boxplot) – サボテンパイソン](https://sabopy.com/py/matplotlib-51/)

## 複数のpngからgifの生成方法 （imageio 使用）

一般的な方法はPillowでGIFを生成する. しかし, 再生時間の長いgifファイルを生成しようとするとエラーが起きる（不安定らしい?）.

- [Python, PillowでアニメーションGIFを作成、保存 | note.nkmk.me](https://note.nkmk.me/python-pillow-gif/)

そこで imageio を使用する. 以下サンプル.

```
gif_path = path + 'out.gif'
frames_path = path + "{i}.png"
with imageio.get_writer(gif_path, mode='I',  fps=60) as writer:
    for i in range(t):
        writer.append_data(imageio.imread(frames_path.format(i=i)))
```
(参考)
- [imageio documentation](https://imageio.readthedocs.io/en/stable/)
- [github imageio](https://github.com/imageio/imageio)

# analyze_shelve.py
## shelveの利用
pickle: オブジェクトのバイトコード化してそのまま保存する方法. そのまま保存するのでロード時にパースする必要がなく便利. 一般的には直列化(serialization)という.

shelve: pickleをデータベースの形式で使えるように拡張したもの. 今回は時系列データを書き出すのでこれを利用した. 注意点はkeyがstr型しか受け付けないこと.

(参考)
- [[python]オブジェクトのピクル(pickle)化 - dackdive's blog](https://dackdive.hateblo.jp/entry/2014/09/16/112404)
- [shelve Python 3.9.1 documentation](https://docs.python.org/3/library/shelve.html)
- [shelve Python Module of the Week](http://ja.pymotw.com/2/shelve/)

# plot_ss.py
## matplotlibで基本となるグラフの要素

- [matplotlibの階層構造を知ると幸せになれる(かもしれない) - Qiita](https://qiita.com/ceptree/items/5fb5e9e6f29d214153c9)

# config.py
## dictを整形してjsonファイル出力
jsonファイルにpythonのdict形式のオブジェクトを書き込むことができる. が, json.dumpをオプションなしで使用すると1行で出力されてしまい, 非常に見ずらい. 整形して出力するにはjson.dumpのオプションでindent=4とする.

(参考)
- [PythonでJSONファイル・文字列の読み込み・書き込み | note.nkmk.me](https://note.nkmk.me/python-json-load-dump/)
- [[python] JSONファイルのフォーマットを整えてDumpする - Qiita](https://qiita.com/Hyperion13fleet/items/7129623ab32bdcc6e203)

## dictの整形: \[\]で囲まれた部分の改行を取り除く

(参考)
- [数値とマッチする正規表現 - Qiita](https://qiita.com/BlueSilverCat/items/f35f9b03169d0f70818b#%E6%95%B4%E6%95%B0)

# gzshelve.py
##  shelve（pickle）の圧縮保存
zlib（データ圧縮ライブラリ）を使ったcompress機能付きshelveを独自で実装した. 
データ処理時間は増えるが, ファイル容量は減る. 作成にあたって, 下記のサイトとpython3.8の標準ライブラリのshelve.pyを参考にした. 

特殊メソッド("magic method")の記述をzlibの機能を使ったものに継承して上書きする. つまり, 　\_\_getitem\_\_\(\)と\_\_setitem\_\_\(\)を継承して書き換えた.
joblibを使う方法もあるらしい?

configファイルnml.jsonで検証. 

|          | 容量                           | 実行時間 |
| -------- | ------------------------------ | -------- |
| 圧縮なし | 115GB                          | 3:48     |
| 圧縮あり | <font color="Red">58GB </font> | 3:40程   |

圧縮ありだと半分ぐらいの容量になっている. 
実行時間は正確な比較にはなっていないが, 致命的に遅くなっていないので圧縮ありの方がよい.

(参考)
- [Python : compress shelve – 圧縮機能付永続辞書 « （有）サウンドボード公式ブログ ](https://memo.jj-net.jp/169)
- [Pythonの特殊メソッド一覧を備忘録としてまとめてみた。 - Qiita](https://qiita.com/y518gaku/items/07961c61f5efef13cccc)


##  zipによる圧縮保存
30分で115GB->14GBまで圧縮可能.
だが, gif生成をいざしようとなったときにその度ごとに30分以上のオーバーヘッドが乗るのは効率が悪いと判断して, 今回はzipによる圧縮は採用していない.

(参考)
- [ZIPを作成する (zipfile, shutil) | まくまくPythonノート](https://maku77.github.io/python/io/create-zip.html)