import pandas as pd


def clean_data():
    # 显示的最大行数和列数，如果超额就显示省略号，这个指的是多少个dataFrame的列。
    # pd.set_option('display.max_rows', 30000)
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', None)
    pd.set_option("display.unicode.ambiguous_as_wide", True)  # 输出列表标签与列对齐
    pd.set_option("display.unicode.east_asian_width", True)  # 输出列表标签与列对齐

    # 读取爬虫文件夹下的recruit_info_all.csv文件
    data = pd.read_csv(open("../爬虫/recruit_info_all.csv", encoding="gbk"), sep=',', header=0)

    # 数据清洗前有的数据
    print('数据清洗前有%d条数据' % data.size)

    # 开始清洗
    data.dropna(axis=0, inplace=True, how='all')  # 删除全是空行的数据
    data.drop(['招聘状态', '联系人'], axis=1, inplace=True)  # 删除“招聘状态”和“联系人”列
    data.drop_duplicates(inplace=True)  # 删除重复行
    # 分割工作地点列
    workplace = data['工作地点'].str.split("-", expand=True)  # 按字符-分割列
    data['工作地点'] = workplace[0]
    # data['具体地点']=workplace[1]
    # 分割参考薪资列
    salary = data['参考薪资'].str.split("-", expand=True)  # 按字符-分割列
    data['最低薪资(k)'] = salary[0]
    data['最高薪资(k)'] = salary[1].str.split("k", expand=True)[0]
    data['总薪'] = salary[1].str.split("·", expand=True)[1].str.split("薪", expand=True)[0]
    data.drop('参考薪资', axis=1, inplace=True)  # 删除“参考薪资”列
    # 分割学历经验列
    exp = data['学历经验'].str.split("-", expand=True)  # 按字符-分割列
    data['最低经历(年)'] = exp[0]
    data['最高经历(年)'] = exp[1].str.split("年", expand=True)[0]
    data['学历要求'] = exp[1].str.split("年", expand=True)[1]
    data.drop('学历经验', axis=1, inplace=True)
    # 分割最低经历(年)
    stop = ['限', '年以下', '年以上']
    old = ['经验不', '一', '10']
    new = ['0', '0.5', '10']
    for i in range(len(stop)):
        explow = data['最低经历(年)'].str.split("{}".format(stop[i]), expand=True)  # 按字符-分割列
        data['最低经历(年)'] = explow[0]
        data['学历要求temp'] = explow[1]
        data['最低经历(年)'].replace("{}".format(old[i]), "{}".format(new[i]), inplace=True)
        data['学历要求temp'].fillna('', inplace=True)  # 数据替换
        data['学历要求'].fillna('', inplace=True)  # 数据替换
        data['学历要求'] = data['学历要求'] + data['学历要求temp']  # 合并'学历要求'列
        del data['学历要求temp']
    # 分割公司信息
    exp = data['公司信息'].str.split("|", expand=True)  # 按字符-分割列
    data['公司信息'] = exp[1]
    # 列名重排
    data = data[["职位名称", "公司名称", "工作地点", "最低薪资(k)", "最高薪资(k)", "总薪", "最低经历(年)", "最高经历(年)", "学历要求", "公司信息"]]
    # 将"职位名称"作为索引
    data.index = data['职位名称']
    del data['职位名称']
    #填充缺失值
    data['最高薪资(k)'].fillna('面议', inplace=True)  # 数据替换
    data['总薪'].fillna('12', inplace=True)  # 数据替换
    data['最高经历(年)'].fillna('最低经历以上', inplace=True)  # 数据替换
    data['学历要求'].replace('学历不','学历不限',inplace=True)  # 数据替换
    data = data[~data['最低薪资(k)'].isin(['面议'])]# 删除'最低薪资(k)'为面议的行

    data.to_excel("预处理文件.xlsx")  # 将数据存入xlsx文件中
    print("清洗后成功存入预处理文件!")

    print('数据清洗后有%d条数据' % data.size)
    print(data[:])


if __name__ == '__main__':
    clean_data()
