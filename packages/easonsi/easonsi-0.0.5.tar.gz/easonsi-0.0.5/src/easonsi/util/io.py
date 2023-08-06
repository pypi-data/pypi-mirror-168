import os, re, sys, random, urllib.parse, json
from collections import defaultdict

""" 
SaveJson, LoadJson: 封装了 json.dump, json.load
SaveJsonl, LoadJsonl: 每行元素为 JSON, 也即 .jsonl 文件
SaveList, LoadList, LoadSet: 每行元素为字符串
SaveCSV, LoadCSV: 每行元素为列表, 按照 sep 进行分割
SaveDict, LoadDict:
"""

# =================== JSON ===================
def SaveJson(obj, ofn, indent=2):
    with open(ofn, "w", encoding = "utf-8") as fout:
        json.dump(obj, fout, ensure_ascii=False, indent=indent)

def LoadJson(fn):
    with open(fn, encoding = "utf-8") as fin:
        return json.load(fin)

# =================== list, jsonl ===================
# 按行分割
def LoadList(fn):
    """ 读取按行分割的文件, 元素为字符串 """
    with open(fn, encoding="utf-8") as fin:
        st = list(ll for ll in fin.read().split('\n') if ll != "")
    return st

def LoadSet(fn):
    """ 相较于 LoadList 输出为 set """
    with open(fn, encoding="utf-8") as fin:
        st = set(ll for ll in fin.read().split('\n') if ll != "")
    return st

def LoadListg(fn):
    with open(fn, encoding="utf-8") as fin:
        for ll in fin:
            ll = ll.strip()
            if ll != '': yield ll

def SaveList(st, ofn):
    """ 保存为按行分割的列表
    列表元素: str """
    with open(ofn, "w", encoding = "utf-8") as fout:
        for k in st:
            fout.write(str(k) + "\n")

def LoadJsonlg(fn): return map(json.loads, LoadListg(fn))
def LoadJsonl(fn): return list(LoadJsonlg(fn))
def SaveJsonl(st, ofn): 
    """ 保存按行分割的 JSON 元素
    注意仅能保存 JSON 支持的类型, 如 tuple 将转为 list"""
    return SaveList([json.dumps(x, ensure_ascii=False) for x in st], ofn)

# =================== CSV ===================
def WriteLine(fout, lst, sep='\t'):
    fout.write(sep.join([str(x) for x in lst]) + '\n')

def LoadCSV(fn, sep=", "):
    ret = []
    with open(fn, encoding='utf-8') as fin:
        for line in fin:
            lln = line.rstrip('\r\n').split(sep)
            ret.append(lln)
    return ret

def LoadCSVg(fn, sep=", "):
    with open(fn, encoding='utf-8') as fin:
        for line in fin:
            lln = line.rstrip('\r\n').split(sep)
            yield lln

def SaveCSV(csv, fn, sep=", "):
    """ 保存二维数组, 文件每一行为一个 list, 按照 sep 进行分割
    默认 sep=`,` 此时将文本中的 `,` 转为， """
    with open(fn, 'w', encoding='utf-8') as fout:
        for x in csv:
            if ',' in sep:
                x = [str(i).replace(",", "，") for i in x]
            WriteLine(fout, x, sep)

# =================== dict ===================
def LoadDict(fn, func=str, sep="\t"):
    dict = {}
    with open(fn, encoding = "utf-8") as fin:
        for lv in (ll.split(sep, 1) for ll in fin.read().split('\n') if ll != ""):
            dict[lv[0]] = func(lv[1])
    return dict

def SaveDict(dict, ofn, sep="\t", output0=True):
    """ 保存字典为按行分割的列表
    注意 key, value 都会转为 str """
    with open(ofn, "w", encoding = "utf-8") as fout:
        for k in dict.keys():
            if output0 or dict[k] != 0:
                fout.write(str(k) + sep + str(dict[k]) + "\n")

# =================== JSON ===================


