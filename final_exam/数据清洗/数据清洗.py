import pandas as pd

def clean():
    # 显示的最大行数和列数
    pd.set_option('display.max_rows', 30000)
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', None)

    # 数据读取
    data=pd.read_csv("../爬虫/网络小说信息数据.csv")
    print("数据清洗前有%d条数据"%data.size)

    # 删除重复行、删除空行列
    data.drop_duplicates(inplace=True)
    data.dropna(axis=0, how='all', inplace=True)
    data.dropna(axis=1, how='all', inplace=True)

    # 清洗“总打赏(单位万)”列
    data['总打赏(单位万)'] = data['总打赏(单位万)'].str.replace('万', '')

    # 清洗“好评人数”列
    data['好评人数'] = data['好评人数'].str.replace('人', '')

    # 将"名称"作为索引
    data.index = data['名称']
    del data['名称']

    # 删除'评分'列
    del data['评分']

    # 将数据存入xlsx文件中
    data.to_excel("预处理文件.xlsx")
    print("数据清洗后有%d条数据" % data.size)

if __name__ == '__main__':
    clean()