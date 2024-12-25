#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file      : xmindReade
# @author    : xiaoduojiao
# @time      : 2024/12/23 20:56
import json
import time

from xmindparser import xmind_to_dict

class Ximd_to_ExcleTestCase:
    def __init__(self,file):
        self.file = file
        self.path = self.file.rsplit('.',1)[0]
        self.file_excel = self.path+str(int(time.time()))+'.xlsx'

    def readXimd(self):
        content = xmind_to_dict(self.file)
        return content[0]['topic']['topics']

    def ximdAnalysis(self,v):
        l = []
        flag = 0
        for i in v:
            if 'topics' in i.keys(): # 如果有子节点则处理如下
                if len(i['topics'])>1: # 如果子节点有两个，则铺展成两个
                    l = l + [{"title":i['title'],"topics":[j]} for j in  i['topics']]
                    flag += 1
                elif len(i['topics'])==1 and i['topics'][0]['title'][:2]=='d:':  # 如果子节点为一个，且下级子节点为目录，则合并目录
                    if i['title'][:2]=='d:': i['title']=i['title'][2:]
                    i['topics'][0]['title'] = f"{i['title']}>{i['topics'][0]['title'][2:]}"
                    l = l + i['topics']
                    flag += 1
                elif len(i['topics'])==1 and i['topics'][0]['title'][:2]!='d:': # 如果子节点为一个，且下级子节点为用例标题，则不做处理
                    if i['title'][:2] == 'd:': i['title'] = i['title'][2:]
                    l = l + [i]
        if flag == 0:
            return v
        else:
            return self.ximdAnalysis(l)
    def compile(self,s:str,l: list): # 如果字符串包含列表中一个元素则返回False
        for i in l:
            if i in s:
                return False
        else:
            return True
    def wrigtExcel(self,l:list):
        data = {
            "用例分组": [i['title'] for i in l],
            "用例名称": [i['title'] +'-'+i['topics'][0]['title'] for i in l],
            "用例等级": [''.join([j['title'][2:] for j in i['topics'][0]['topics'] if 'P:' in j['title']]) if 'topics' in i['topics'][0].keys() else '' for i in l],
            "用例标签": ['' for i in l],
            "前置条件": ['' for i in l],
            "测试步骤":['\n'.join([f"{n+1}、"+j['title'] for n,j in enumerate(i['topics'][0]['topics']) if  self.compile(j['title'],['P:','r:']) ]) if 'topics' in i['topics'][0].keys() else '' for i in l],
            "预期结果":['\n'.join([f"{n+1}、"+j['topics'][0]['title'] if 'topics' in j.keys() else ''  for n,j in enumerate(i['topics'][0]['topics']) if  self.compile(j['title'],['P:','r:']) ])  if 'topics' in i['topics'][0].keys() else '' for i in l],
            "备注":[''.join([j['title'][2:] for j in i['topics'][0]['topics'] if 'r:' in j['title'] ]) if 'topics' in i['topics'][0].keys() else '' for i in l],
        }
        import pandas as pd
        df = pd.DataFrame(data)
        df.to_excel(self.file_excel, index=False)

    def run(self):
        v = self.readXimd()
        l = self.ximdAnalysis(v)
        print(self.file_excel)
        self.wrigtExcel(l)

if __name__ == '__main__':
    Ximd_to_ExcleTestCase(file=r'C:\Users\XDJ\Desktop\V2.425.0件量分析二期(冒烟测试用例).xmind').run()
