import pandas as pd

def analysis_data():
    # 显示的最大行数和列数,如果超额就显示省略号,这个指的是多少个dataFrame的列。
    # pd.set_option('display.max_rows', 30000)
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width',None)
    # pd.set_option("display.unicode.ambiguous_as_wide", True)  # 输出列表标签与列对齐
    # pd.set_option("display.unicode.east_asian_width", True)  # 输出列表标签与列对齐

    # cate=['算法','数据分析','安卓','大数据','嵌入式','架构师','前端','ios','java','运维','产品经理','项目经理','python']

    # 读取文件
    data=pd.read_excel("预处理文件.xlsx")

    nav=['职位名称','公司名称','工作地点','学历','日期']
    for i in range(len(nav)):
        print(data['{}'.format(nav[i])].value_counts(),'\n')

    salarylow = data.groupby(by=['学历'])['最低月薪'].mean()
    salaryhigh = data.groupby(by=['学历'])['最高月薪'].mean()
    print(salarylow,salaryhigh)

    # print(data)

if __name__ == '__main__':
    analysis_data()