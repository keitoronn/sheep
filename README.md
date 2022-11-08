
# Sheep Shepherding Program 
Sheep Shepherding Program for 2021 bachelor thesis

日本語のREADMEはこちら [README_JP.md](README_JP.md)

# Features

* Demo mode 

  you can check the status of similation with matplotlib animation.
* Normal mode
  
  You can set parameter and run many trials in multi-process. 

# Requirement
 
* Python 3.6.5 or higher
 
Environments under Linux Ubuntu is tested.
 
# Installation
 
Install packages with pip command.
 
```bash
pip3 install -r requirement.txt
```

# Docker 
build docker image
```bash
docker-compose build
```
start docker container 
```bash
docker-compose up -d
```
enter docker container
```bash
docker-compose exec python3 bash
```

# Usage
 
Use this command for usage help .

```bash
python3 main.py -h
```
 
## Demo 
Note：This function is only availabe in GUI environment.

Use this command for demo mode. 

In demo mode, you can check animation of similation.
 
```bash
python3 main.py -d
```

## Set Config File
You can set parameter of similation using config files. 

For instance, use this command to set config file "config/test.json".


Caution:it takes a long time (more than 10 hours) to execute the program depending on the parameters.
```bash
python3 main.py -p "config/test.json"
```

## Config File
You can make own config files. 

See [here](docs/config_file_format.md) for more details. An example is here.

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
If you set config file using -p option, log files are generated.

The contents of the log file are location of all sheep and shepherd at all times.

If you use -c option, csv format is selected. Default is shelve(Pickle) format. 

See  [Python Document of shelve format](https://docs.python.org/ja/3/library/shelve.html)
 for details of shelve format. 

### NOTE: File size of shelve files is sometimes too large depending on similation time. It may be better to use csv format. Also, you cannot see the contents of the shelve file. But shelve format has the advantage of being easy to code for file cotent.

Log files path is "log/yyyy_mmdd_hhmmss/data/". Directory structure is as follows. 
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
succuss rate is written in "log/yyyy_mmdd_hhmmss/result.csv".
You can see summary of results of similation. Path is "log/yyyy_mmdd_hhmmss/graph/".

Type of graph 

 graph name     |  description
---- | ----
 distance_max   | Box plot. Maximum distance from goal for all sheep at the end of simulation.
 distance_mean  | Box plot. Average distance from goal for all sheep at the end of simulation.
 success_time   | Box plot of success time
 patch_plot     | Patch plot. Sheep and shepherd position at the end of the failed simulation.


## GIF
If you want to generate gif file of similation, use gif.py. 
Output path of gif file is "log/yyyy_mmdd_hhmmss/gif/".
```bash
python3 gif.py [directory path]
```

see usage help for more detail.
```bash
python3 gif.py -h
```

# Dependencies
* numpy
* matplotlib
* imageio
 
# Note
 
I don't test environments under Windows and Mac.
 
# License
 
"Sheep-Shepherding Program" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
 