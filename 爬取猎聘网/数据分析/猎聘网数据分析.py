import pandas as pd

def analysis_data():
    # 显示的最大行数和列数,如果超额就显示省略号,这个指的是多少个dataFrame的列。
    # pd.set_option('display.max_rows', 30000)
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width',None)
    # pd.set_option("display.unicode.ambiguous_as_wide", True)  # 输出列表标签与列对齐
    # pd.set_option("display.unicode.east_asian_width", True)  # 输出列表标签与列对齐

    # "java","python","数据分析","算法","Android","前端"
    # 北京、上海、南京、苏州﹑杭州﹑武汉、广州、深圳

    # 读取文件
    data=pd.read_excel("预处理文件.xlsx")

    beijing = data[data['工作地点'].isin(['北京'])]
    shanghai = data[data['工作地点'].isin(['上海'])]
    nanjing = data[data['工作地点'].isin(['南京'])]
    suzhou = data[data['工作地点'].isin(['苏州'])]
    hangzhou = data[data['工作地点'].isin(['杭州'])]
    wuhang = data[data['工作地点'].isin(['武汉'])]
    guangzhou = data[data['工作地点'].isin(['广州'])]
    shenzhen = data[data['工作地点'].isin(['深圳'])]

    # print(beijing,shanghai,nanjing,suzhou,hangzhou,wuhang,guangzhou,shenzhen)

    # print(data['职位名称'].value_counts())
    # print(data['公司名称'].value_counts())
    # print(data['工作地点'].value_counts())
    # print(data['最低薪资(k)'].value_counts())
    # print(data['最高薪资(k)'].value_counts())
    # print(data['总薪'].value_counts())
    # print(data['最低经历(年)'].value_counts())
    # print(data['最高经历(年)'].value_counts())
    # print(data['学历要求'].value_counts())
    # print(data['公司信息'].value_counts())

    print("原数据".center(100, "—"), '\n', data)
    print("所获取信息中关于每个地区的数据条目数".center(100, "—"), '\n', data['工作地点'].value_counts())

    sorts = ["java", "python", "数据分析", "算法", "Android", "前端"]

    print("所获取信息中关于每个类别的公司数量".center(100, "—"))
    tempStr=["java"or"JAVA"or"Java","python"or"Python"or"PYTHON","数据分析","算法","Android"or"安卓"or"android","前端"]
    for i in range(len(sorts)):
        print_name = data["职位名称"].str.contains(tempStr[i])
        number = print_name[print_name == 1].index
        print("关于'{}'的公司共有{}个".format(sorts[i],len(number)))

    print("所获取信息中关于学历要求统计".center(100, "—"))
    tempStr=['学历不限','大专及以上','统招本科','本科及以上','硕士及以上','博士']
    for i in range(len(tempStr)):
        print_name = data["学历要求"].str.contains(tempStr[i])
        number = print_name[print_name == 1].index
        print("岗位需'{}'的公司共有{}个".format(tempStr[i],len(number)))

    print("所获取信息中关于公司类型统计".center(100, "—"))
    tempStr = ['计算机软件','大数据','云计算','个工智能','互联网金融','互联网/电商','IT服务','电子商务','计算机/网络设备','企业服务软件','互联网+','通信业','电子/芯片/半导体']
    for i in range(len(tempStr)):
        print_name = data["公司信息"].str.contains(tempStr[i])
        number = print_name[print_name == 1].index
        print("公司类型为'{}'的共有{}个".format(tempStr[i], len(number)))

    print("所获取信息中关于最低经验的统计".center(100, "—"))
    e01=len(data[data['最低经历(年)']<1])
    e2=len(data[(data['最低经历(年)']>=1)&(data['最低经历(年)']<2)])
    e35=len(data[(data['最低经历(年)']>=3)&(data['最低经历(年)']<5)])
    e5=len(data[(data['最低经历(年)']>=5)])
    print("经历不限的岗位有：{}个\n最低经验在1~2年的有：{}个\n"
          "最低经验在3~5年的有：{}个\n最低经验不低于5年的有：{}个".format(e01,e2,e35,e5))

    print("所获取信息中关于学历".center(100, "—"), '\n', data['学历要求'].value_counts())
    print("所获取信息中关于公司类型".center(100, "—"), '\n', data['公司信息'].value_counts())


if __name__ == '__main__':
    analysis_data()

