import pandas as pd

def analysis():
    # 显示的最大行数和列数
    pd.set_option('display.max_rows', 30000)
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', None)

    raw_data=pd.read_excel("../数据清洗/预处理文件.xlsx")

    columns=['总阅读数','总鲜花数','总催更票数','总打赏(单位万)','总月票数','总分享次数','好评人数',]

    # 最高top10小说
    for i in range(len(columns)):
        print("{}最高的10本小说".format(columns[i]).center(50,'-'))
        print(raw_data.sort_values(by=['{}'.format(columns[i])], ascending=False)[['名称','{}'.format(columns[i])]][0:10])

    # 小说分类统计
    print("小说分类".center(50, '-'))
    print(raw_data['小说分类'].value_counts())

    # 小说类型统计
    print("小说类型统计".center(50, '-'))
    print(raw_data.groupby(['小说分类']).mean())
    print(raw_data.groupby(['小说分类']).mean().index.tolist())
    print(raw_data.groupby(['小说分类']).mean()['总阅读数'].tolist())

    # print(raw_data)

if __name__ == '__main__':
    analysis()