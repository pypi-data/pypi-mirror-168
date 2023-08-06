from .util.io import (
    SaveJsonl, LoadJsonl, LoadJsonlg,
    SaveJson, LoadJson,
    SaveCSV, LoadCSV, LoadCSVg,
    SaveList, LoadList, LoadListg, LoadSet,
    SaveDict, LoadDict,
)
from .util.network import *
from .util.file import (
    # 筛选, 排序. 返回结果, 并可选是否写入 ofn
    SelectRowsbyCol, SortRows,
    # 合并, 去重, 采样. 输出为 ofn
    MergeFiles, JoinFiles, RemoveDupRows, SampleRows,
)

""" 

"""

import numpy as np
# import sklearn.utils

def Sample(data, num, seed=0, replace=False):
    """ 从 list 数据中随机抽取 num 个数据
    replace: 是否有放回抽样"""
    np.random.seed(seed)
    data = np.random.shuffle(data)
    if replace==False and num > len(data):
        print(f'[Warning] 不放回抽样不允许, 返回 shuffle 后的全量数据. num > len(data), num: {num}, len(data): {len(data)}')
        return data
    # return np.random.choice(data, num, replace=replace)
    return data[:num]

def SplitTrainTest(data, ratio=0.8, seed=0):
    """ 将数据集按照 ratio 分成训练集和测试集 """
    np.random.seed(seed)
    np.random.shuffle(data)

    n = len(data)
    train_num = int(n * ratio)
    return data[:train_num], data[train_num:]

def IsChineseStr(z):
    """ 判断是否为中文字符: [\u4e00-\u9fa5] """
    return re.search('^[\u4e00-\u9fa5]+$', z) is not None

def ChineseCutSent(para):
    """ 中文分句, from https://blog.csdn.net/blmoistawinde/article/details/82379256 """
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)    # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)        # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)        # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return [l.strip() for l in para.split("\n") if l.strip()]

def FreqDict2List(dt):
    """ 将 Counter 按照 value 排序, 转为 list
    例如输出 [("value_1", 3), ("value_2", 2)]"""
    return sorted(dt.items(), key=lambda d:d[-1], reverse=True)

def CalcF1(correct, output, golden: int, returnStr=False):
    """ 计算 F1 等指标
    输入: TP, P, T
    输出: returnStr 控制输出值还是指标的描述 """
    prec = correct / max(output, 1);  reca = correct / max(golden, 1);
    f1 = 2 * prec * reca / max(1e-9, prec + reca)
    if returnStr:
        pstr = 'Prec: %.4f %d/%d, Reca: %.4f %d/%d, F1: %.4f' % (prec, correct, output, reca, correct, golden, f1)
        return pstr
    else:
        return f1, prec, reca

class TokenList:
    """ 定义 token 列表 """
    def __init__(self, file, low_freq=2, source=None, func=None, save_low_freq=2, special_marks=[]):
        """ 
        file: 每一行为 `token\tfrequence`
        以下参数仅在 file 为 None 时有效
            source 为所有原始词的列表; func 对每个词进行筛选; 最终 source 处理后词频 >=save_low_freq 的保留
            special_marks: 额外定义的特殊 token"""
        if not os.path.exists(file):
            tdict = defaultdict(int)
            # 设置 special_marks 一个较高的频次, 以保留
            for i, xx in enumerate(special_marks): tdict[xx] = 100000000 - i
            for xx in source:
                for token in func(xx): tdict[token] += 1
            tokens = FreqDict2List(tdict)
            tokens = [x for x in tokens if x[1] >= save_low_freq]
            SaveCSV(tokens, file)
        self.id2t = ['<PAD>', '<UNK>'] + \
            [x for x,y in LoadCSV(file) if float(y) >= low_freq]
        self.t2id = {v:k for k,v in enumerate(self.id2t)}
    def get_id(self, token): return self.t2id.get(token, 1)
    def get_token(self, ii): return self.id2t[ii]
    def get_num(self): return len(self.id2t)

