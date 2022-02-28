#网络小说数据清分析

import pandas as pd
import numpy as np

#初始化数据
def init_data():
    data = pd.read_csv('网络小说信息数据.csv', encoding='utf-8')
    return data

#根据分组函数对类型进行分组
#并根据分组的数据获取多个平均值
def group_by_type_average(data):
    #按照小说分类取得各个分类的平均值
    average = data.groupby(['小说分类']).mean()
    # print(average)
    average.to_csv('网络小说类型平均值数据.csv', encoding='utf-8')

#根据分组函数对类型进行分组
#并根据分组的数据取得各个分类的总和
def gourp_by_type_sum(data):
    #按照小说分类取得各个分类的总和
    sum = data.groupby(['小说分类']).sum()
    # print(sum)
    sum.to_csv('网络小说类型总和数据.csv', encoding='utf-8')

#根据分组函数对类型进行分组
#并根据分组的数据取得各个分类的小说的数量
def gourp_by_type_count(data):
    #按照小说分类取得各个分类的数量
    count = data.groupby(['小说分类']).count()
    # print(count)
    count_list = []
    #将每个分类的数量单独取出并赋值
    list = count['id'].values.tolist()
    for i in list:
        count_list.append(i)
    count['小说数量'] = list
    # print(count)
    count['小说数量'].to_csv('网络小说类型数量数据.csv', encoding='utf-8')

if __name__ == '__main__':
    data = init_data()

    #根据分组函数对类型进行分组并根据分组的数据获取多个平均值
    # group_by_type_average(data)

    #根据分组函数对类型进行分组并根据分组的数据取得各个分类的总和
    # gourp_by_type_sum(data)

    #根据分组函数对类型进行分组并根据分组的数据取得各个分类的小说的数量
    # gourp_by_type_count(data)
