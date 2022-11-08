
# Config file format

## English ver

Note: Please write it in json format. An example is [config/demo.json](../config/demo.json)

item  |  description | value
---- | ---- | ----
shepherd_model   | Shepherd model. You can select "farthest-agent tageting" or proposed model "collective"| "farthest-agent" or "collective"
process_number  |  Number of processes to be used when using multiprocess (multiprocessing.Pool) | int
trial_number   | Number of attempts| int
sheep_number   | Number of sheep | int
slow_sheep_number  | Number of sheep not responding to shepherd | list 
n_iter | Limit time for similation | int
goal | Center position of goal zone | list 
goal_radius | Radius of goal zone | float 
shepherd_initial_pos | Initial position of shepherd | int
sheep_initial_pos_radius | Radius of "the circle placement" in the initial state of the sheep　  | float 
sheep_initial_pos_base | Center of "the circle placement" in the initial state of the sheep| list
sheep_param | parameter of sheep responding to shepherd | list 
slow_sheep_param | parameter of sheep not responding to shepherd | list
shepherd_param | parameter of shepherd | list

"the circle placement" : Randomly placed in an area within a circle according to a uniform distribution
## 日本語 ver
json形式で書いてください. 例は [config/demo.json](../config/demo.json)

項目  |  説明 | 値
---- | ---- | ----
shepherd_model   | 牧羊犬のモデル. "farthest-agent targeting", または提案モデル"collective" を選べる  | "farthest-agent" or "collective"
process_number  | マルチプロセス(multiprocessing.Pool)使用時に使うプロセス数 | int
trial_number   | 試行回数 | int
sheep_number   | 羊の数 | int
slow_sheep_number  | 牧羊犬に対して反応しない羊の数 | list 
n_iter | イテレーション回数. シミュレーション限界時間 | int
goal | 目的地の中心位置 | list 
goal_radius | 目的地の半径 | int
shepherd_initial_pos | 牧羊犬の初期状態における位置 | list 
sheep_initial_pos_radius | 羊の初期状態における円内配置の半径 | float 
sheep_initial_pos_base | 羊の初期状態における円内配置の中心位置 | list
sheep_param | 反応する羊のパラメータ | list 
slow_sheep_param |  反応しない羊のパラメータ | list
shepherd_param | 牧羊犬のパラメータ | list

羊の円内配置 : 一様分布に従い円内の領域にランダムに配置