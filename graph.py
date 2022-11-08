import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
import matplotlib.colors as colors
import csv

from sheep_shepherding.util import config
from sheep_shepherding.util import analyze

def gen_graph_rho(file_path, fig_file_name):
    '''
    rhoに関するグラフ
    '''
    fig, ax = plt.subplots()
    pts = []
    y_datas = []
    labels = []
    styles = []
    #colors = []
    with open(file_path, encoding='utf_8') as f:
        reader = csv.reader(f, delimiter=',')
        trial = 0
        for row in reader:
            labels.append(row[0])
            styles.append(row[1])
            y_data = [int(s) for s in row[2:]]
            y_datas.append(y_data)

    for i in range(len(y_datas)):
        #x = [i+1 for i in range(0, len(y_datas[i]))] 
        x = [(j+1)/(len(y_datas[i])*2) for j in range(0, len(y_datas[i]))]
        y = y_datas[i]
        line, color, marker = set_style(styles[i], fixed=2)
        a = ax.plot(x, y, color=color, linestyle=line, marker=marker, label=labels[i])
        pts.append(a)
    
    ax.set_xlabel('K/N')
    ax.set_ylabel('Success Rate')
    ax.set_ylim(-5,105)
    #plt.legend(bbox_to_anchor=(0, -0.1), loc='upper left', borderaxespad=0, fontsize=18)
    #plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=18)
    #plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=6)
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=2)
    plt.tight_layout()
    
    #plt.show()
    fig.savefig(fig_file_name, bbox_inches='tight')

def gen_graph_n(file_path, fig_file_name):
    '''
    Nに関するグラフ
    '''
    fig, ax = plt.subplots()
    pts = []
    y_datas = []
    labels = []
    styles = []
    #colors = []
    with open(file_path , encoding='utf_8') as f:
        reader = csv.reader(f, delimiter=',')
        trial = 0
        for row in reader:
            labels.append(row[0])
            styles.append(row[1])
            y_data = [int(s) for s in row[2:]]
            y_datas.append(y_data)

    #rhoをunicodeのu"\u03C1"に
    re_labels = [labels[i].replace("rho", "\u03C1") for i in range(0, len(labels))]

    for i in range(len(y_datas)):
        x = [i+1 for i in range(0, len(y_datas[i]))] 
        y = y_datas[i]
        line, color, marker = set_style(styles[i], fixed=1)
        #print(x,y)
        a = ax.plot(x, y, color=color, linestyle=line, marker=marker, label=re_labels[i])
        pts.append(a)

    plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_xlabel('K')
    ax.set_ylabel('Success Rate')
    ax.set_ylim(-5,105)
    #plt.legend(bbox_to_anchor=(0, -0.1), loc='upper left', borderaxespad=0, fontsize=18)
    #plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=18)
    #plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=6)
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=2)
    plt.tight_layout()
    
    #plt.show()
    fig.savefig(fig_file_name, bbox_inches='tight')

def set_style(str, fixed):
    '''
    line_style, color, marker_styleを決める
    '''
    line = None
    marker = None
    color = None
    # 従来法か提案法
    if str[0]=='p':
        line = "solid"
    else:
        line = "dotted"

    #N
    if str[1]=='l':
        color = "0.7"
    elif str[1]=='m':
        color = "0.5"
    elif str[1]=='h':
        color = "0.1"

    #rho
    if str[2]=='l':
        marker = "x"
    elif str[2]=='m':
        marker = "^"
    elif str[2]=='h':
        marker = "o"
    
    if fixed == 1:
        color = "0.1"
    elif fixed == 2:
        marker = "o"

    return line, color, marker

def gen_graph(file_path, fig_file_name):
    '''
    rとrhoの関係のグラフ
    '''
    fig, ax = plt.subplots()

    y_datas = []
    with open(file_path) as f:
        reader = csv.reader(f, delimiter=',')
        trial = 0
        x_data = next(reader)
        for row in reader:
            y_data = [float(s) for s in row]
            y_datas.append(y_data)

    for i in range(len(y_datas)):
        x = x_data
        y = y_datas[i]
        plt.plot(x, y, marker='o')
    
    #基準線
    plt.hlines(20, xmin=x_data[0], xmax=x_data[-1], linestyles='dashed')
    ax.set_xlabel(u'\u03C1')
    ax.set_ylabel(r'$\overline{r}$')
    #plt.show()
    fig.savefig(fig_file_name)

def success_time_plot_compare(directory_path1, directory_path2, fig_file_name):
    '''
    同じNについて誘導成功時間を比較するグラフ
    '''
    plt.rcParams["mathtext.fontset"] = 'cm'
    plt.rcParams['mathtext.default'] = 'it'
    x = []
    y = []
    z = []
    param = config.load(directory_path1+"/setting.json")
    slow_nums = range(param["slow_sheep_number"][0], param["slow_sheep_number"][1] + 1)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    for slow_num in slow_nums:
        list1 = analyze.get_end_step_list(directory_path1, slow_num, param)
        list2 = analyze.get_end_step_list(directory_path2, slow_num, param)
        x.extend(list1)
        y.extend(list2)
        #x.append([np.log10(i) for i in list1])
        #y.append([np.log10(i) for i in list2])
        z.append([slow_num for i in list1])

    #対数目盛
    ax.set_xscale('log', base=10)
    ax.set_yscale('log', base=10)
    ax.grid(True)

    # カラーマップRdYlBu
    cm = plt.cm.get_cmap('RdYlBu')
    # axに散布図を描画、戻り値にPathCollectionを得る
    boundary = [i for i in range(1, len(slow_nums)+2)]
   
    #ax.grid(which='minor')
    norm = colors.BoundaryNorm(boundary, cm.N, clip=True)
    mappable = ax.scatter(x, y, c=z, s=0.5, cmap=cm, norm=norm)
    # カラーバーを付加
    cbar = fig.colorbar(mappable, ax=ax)
    cbar.set_label("K")

    left, right = plt.xlim()  # return the current xlim
    #print(left, right)
    ax.plot([left,right], [left,right], color='black', linestyle = "dashed", linewidth=0.7)
    ax.set_xlabel(r'$\tau_c$', fontsize=16)
    ax.set_ylabel(r'$\tau_p$', fontsize=16)
   
    #fig_path = "{}/graph/{}.pdf".format(directory_path1, "success_time_compare") 
    fig.savefig(fig_file_name)

def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map"""
    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:
    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)

if __name__ == '__main__':
    #gen_graph("csv/rho.csv", "rho.png")
    gen_graph_n("csv/data.csv", "n50.png")
    #gen_graph_rho("csv/data.csv", "rho10.png")
    #success_time_plot_compare("log/2021_0203_122135", "log/2021_0202_111402", "mm0.pdf")