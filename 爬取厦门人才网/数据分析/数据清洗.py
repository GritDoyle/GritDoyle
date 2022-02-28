import pandas as pd


def clean_data():
    # 显示的最大行数和列数，如果超额就显示省略号，这个指的是多少个dataFrame的列。
    # pd.set_option('display.max_rows', 30000)
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', None)
    pd.set_option("display.unicode.ambiguous_as_wide", True)  # 输出列表标签与列对齐
    pd.set_option("display.unicode.east_asian_width", True)  # 输出列表标签与列对齐

    # 读取爬虫文件夹下的csv文件
    algo=pd.read_csv(open("../爬虫/recruit_info_algo.csv", encoding="gbk"), sep=',', header=0)
    analysis=pd.read_csv(open("../爬虫/recruit_info_analysis.csv", encoding="gbk"), sep=',', header=0)
    android=pd.read_csv(open("../爬虫/recruit_info_android.csv", encoding="gbk"), sep=',', header=0)
    bigdata=pd.read_csv(open("../爬虫/recruit_info_bigdata.csv", encoding="gbk"), sep=',', header=0)
    embed=pd.read_csv(open("../爬虫/recruit_info_embed.csv", encoding="gbk"), sep=',', header=0)
    framework=pd.read_csv(open("../爬虫/recruit_info_framework.csv", encoding="gbk"), sep=',', header=0)
    front=pd.read_csv(open("../爬虫/recruit_info_front.csv", encoding="gbk"), sep=',', header=0)
    ios=pd.read_csv(open("../爬虫/recruit_info_ios.csv", encoding="gbk"), sep=',', header=0)
    java=pd.read_csv(open("../爬虫/recruit_info_java.csv", encoding="gbk"), sep=',', header=0)
    om=pd.read_csv(open("../爬虫/recruit_info_om.csv", encoding="gbk"), sep=',', header=0)
    product=pd.read_csv(open("../爬虫/recruit_info_product.csv", encoding="gbk"), sep=',', header=0)
    project=pd.read_csv(open("../爬虫/recruit_info_project.csv", encoding="gbk"), sep=',', header=0)
    python=pd.read_csv(open("../爬虫/recruit_info_python.csv", encoding="gbk"), sep=',', header=0)

    sorts = ['algo', 'analysis', 'android', 'bigdata', 'embed', 'framework', 'front', 'ios', 'java', 'om', 'product','project', 'python']
    cates = [algo, analysis, android, bigdata, embed, framework, front, ios, java, om, product, project, python]
    # cate=['算法','数据分析','安卓','大数据','嵌入式','架构师','前端','ios','java','运维','产品经理','项目经理','python']

    data=pd.concat(cates,ignore_index=True)
    # 数据清洗前有的数据
    print('数据清洗前有%d条数据' % data.size)

    # 开始清洗
    data.dropna(axis=0, inplace=True, how='all')  # 删除全是空行的数据
    # data.drop(['招聘状态', '联系人'], axis=1, inplace=True)  # 删除“招聘状态”和“联系人”列
    data.drop_duplicates(inplace=True)  # 删除重复行
    # 分割参考薪资列
    salary = data['参考月薪'].str.split("-", expand=True)  # 按字符-分割列
    data['最低月薪'] = salary[0]
    data['最高月薪'] = salary[1].str.split("(", expand=True)[0]
    data['最高月薪'] = data['最高月薪'].str.split("元", expand=True)[0]
    data.drop('参考月薪', axis=1, inplace=True)  # 删除“参考薪资”列
    # 分割发布时间
    time = data['发布时间'].str.split(" ", expand=True)  # 按字符 分割列
    data['日期'] = time[0]
    data['时间'] = time[1]
    data.drop('发布时间', axis=1, inplace=True)  # 删除“发布时间”列
    # 列名重排
    data = data[["职位名称", "公司名称", "工作地点", "最低月薪", "最高月薪", "学历", "日期",'时间']]
    # 将"职位名称"作为索引
    data.index = data['职位名称']
    del data['职位名称']
    # #填充缺失值
    data['最低月薪'].fillna('面谈', inplace=True)  # 数据替换
    data['学历'].fillna('不限', inplace=True) # 数据替换
    data['学历'].replace('无','不限') # 数据替换
    data = data[~data['最低月薪'].isin(['面谈'])]# 删除'最低薪资(k)'为面议的行

    data.to_excel("预处理文件.xlsx")  # 将数据存入xlsx文件中
    print("清洗后成功存入预处理文件!")
    print('数据清洗后有%d条数据' % data.size)
    print(data[:])


if __name__ == '__main__':
    clean_data()
