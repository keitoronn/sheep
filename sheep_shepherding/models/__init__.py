from .sheep import Sheep
from .shepherd import Shepherd
from .collective_shepherd import Collective_Shepherd

def select_shepherd_model(name, init_param):
    '''
    Shepherdモデルの選択 当該クラスを初期化して返す
    '''
    if name == "farthest_agent":
        return Shepherd(init_param)
    elif name == "collective":
        return Collective_Shepherd(init_param)
    else:
        raise Exception('Invalid shepherd model selected.')