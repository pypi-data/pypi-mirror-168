import os, re, sys, random, urllib.parse, json
from collections import defaultdict

from .io import LoadCSV

""" 
RemoveDupRows: 去重. 
SelectRowsbyCol: 筛选. 筛选 CSV 文件中某一列满足某些条件的行
SortRows: 排序. 根据 CSV 文件的某一列排序

MergeFiles: 合并匹配的文件
JoinFiles: join 两份 CSV 文件

SampleRows: 抽样若干行
"""

def MergeFiles(dir, ofn, regstr = ".*"):
    """ 合并目录下的匹配到的文件, 并保存到 objfile 中
        regstr: 例如 ".*\.json.*" 匹配 .json, .jsonl 等
    输出: ofn"""
    with open(ofn, "w", encoding = "utf-8") as fout:
        for file in os.listdir(dir):
            if re.match(regstr, file):
                with open(os.path.join(dir, file), encoding = "utf-8") as filein:
                    fout.write(filein.read())

def SelectRowsbyCol(fn, ofn=None, st=[], num = 0, sep = "\t"):
    """ 筛选第 num 列中包含 st 的行, 并保存到 ofn 中
        st: 为列表, 筛选条件为 line[num] in st
    返回: 筛选后的结果
    """
    result = []
    with open(fn, encoding = "utf-8") as fin:
        for line in (ll for ll in fin.read().split('\n') if ll != ""):
            d = line.split(sep)
            if d[num] in st:
                result.append(d)
    if ofn is not None:
        with open(ofn, "w", encoding = "utf-8") as fout:
            for d in result:
                fout.write(sep.join(d) + '\n')
    return result

def RemoveDupRows(fn, ofn='*'):
    """ 行级别的去重
    输出: ofn. 若为 '*' 则替换原 fn 文件"""
    st = set()
    if ofn == '*': ofn = fn
    with open(fn, encoding = "utf-8") as fin:
        for line in fin.read().split('\n'):
            if line.strip() == "": continue
            st.add(line.strip())
    with open(ofn, "w", encoding = "utf-8") as fout:
        for line in st:
            fout.write(line + '\n')

def JoinFiles(fnx, fny, ofn, sep = "\t"):
    """ join 两份 CSV 文件
    输出: ofn"""
    with open(fnx, encoding = "utf-8") as fin:
        lx = [vv for vv in fin.read().split('\n') if vv != ""]
    with open(fny, encoding = "utf-8") as fin:
        ly = [vv for vv in fin.read().split('\n') if vv != ""]
    with open(ofn, "w", encoding = "utf-8") as fout:
        for i in range(min(len(lx), len(ly))):
            fout.write(lx[i] + sep + ly[i] + "\n")


def SortRows(fn, ofn=None, cid=0, type=int, reverse = True, sep = "\t"):
    """ 根据 CSV 文件的第 cid 列排序
    返回: 排序后的列表"""
    lines = LoadCSV(fn)
    dat = []
    for dv in lines:
        if len(dv) <= cid: continue
        dat.append((type(dv[cid]), dv))
    result = []
    for dd in sorted(dat, reverse=reverse):
        result.append(dd)
    if ofn is not None:
        with open(ofn, "w", encoding = "utf-8") as fout:
            for dd in result:
                fout.write(sep.join(dd[1]) + '\n')
    return result

def SampleRows(fn, num, ofn, seed=0):
    """ 从文件中抽取 num 行
    输出: ofn"""
    zz = list(open(fn, encoding='utf-8'))
    num = min([num, len(zz)])
    random.seed(seed)
    zz = random.sample(zz, num)
    with open(ofn, 'w', encoding='utf-8') as fout:
        for xx in zz: fout.write(xx)