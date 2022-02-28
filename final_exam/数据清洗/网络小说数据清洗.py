#网络小说数据清洗

import pandas as pd
import numpy as np
import re,random,csv

#从文本中获取数据
def get_data():
    #从csv文件中获取数据
    data = pd.read_csv('网络小说信息数据.csv', encoding='utf-8')
    #打印csv中数据总数量(数据清洗前)
    print("数据清洗前共有%s条数据" % data.size)
    #数据清洗
    clean_data(data)

def clean_data(data):
    #去除重复数据
    data.drop_duplicates(inplace = True)
    #将总打赏中带有"万"字的转为数字
    reward_list = data['总打赏(单位万)'].values.tolist()
    reward_list_cleaned = []
    for reward in reward_list:
        if "万" in reward:
            count = reward[0:-1]
            result = float(count) * 10000
        else:
            count = float(reward)
            result = count * 10000
        reward_list_cleaned.append(result)
    # print(reward_list_cleaned)
    data['总打赏(单位万)'] = reward_list_cleaned
    # print(data['总打赏(单位万)'])
    #数据清洗后csv中的数据数量
    print("数据清洗后共有%s条数据" % data.size)
    #写入csv文件
    data.to_csv('网络小说信息数据.csv',encoding = 'utf-8')

if __name__ == '__main__':
    get_data()