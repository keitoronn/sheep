# permission deniedのエラーが出た場合は chmod +x do.sh
# nohupでサーバーからexitした後もプログラムを動かすことができる　
nohup python3 main.py -p "./config/pll.json" -c
nohup python3 main.py -p "./config/plm.json" -c
nohup python3 main.py -p "./config/plh.json" -c
#nohup python3 main.py -p "./config/pml.json" -c
#nohup python3 main.py -p "./config/pmm.json" -c
#nohup python3 main.py -p "./config/pmh.json" -c
#nohup python3 main.py -p "./config/phl.json" -c
#nohup python3 main.py -p "./config/phm.json" -c
#nohup python3 main.py -p "./config/phh.json" -c