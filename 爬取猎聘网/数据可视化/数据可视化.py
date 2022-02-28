import pandas as pd
from pyecharts.charts import Bar, Page, Pie, Line, Funnel, WordCloud
from pyecharts import options as opts

pd.set_option('display.max_rows', 30000)
data=pd.read_excel("../数据分析/预处理文件.xlsx")

# print(data['职位名称'].value_counts())
data['公司名称'].value_counts()
data['工作地点'].value_counts()
data['最低薪资(k)'].value_counts()
data['最高薪资(k)'].value_counts()
data['总薪'].value_counts()
data['最低经历(年)'].value_counts()
data['最高经历(年)'].value_counts()
data['学历要求'].value_counts()
data['公司信息'].value_counts()

def 每个地区的数据条目数():
    data['工作地点'].value_counts()
    bar = Bar()
    x,y=[],[]
    for i in range(len(data['工作地点'].value_counts().index)):
        x.append(data['工作地点'].value_counts().index[i])
        y.append(int(data['工作地点'].value_counts()[i]))
    bar.add_xaxis(x)
    bar.add_yaxis("数量",y)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="每个地区的数据条目数"))
    return bar

def 每个类别的公司数量():
    sorts = ["java", "python", "数据分析", "算法", "Android", "前端"]
    tempStr = ["java" or "JAVA" or "Java", "python" or "Python" or "PYTHON", "数据分析", "算法", "Android"or"安卓"or"android", "前端"]
    tempNum=[]
    for i in range(len(sorts)):
        print_name = data["职位名称"].str.contains(tempStr[i])
        number = print_name[print_name == 1].index
        tempNum.append(len(number))
    pie=(
        Pie()
            .add("", [list(z) for z in zip(tempStr, tempNum)])
            .set_global_opts(title_opts=opts.TitleOpts(title="每个类别的公司数量"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return pie

def 学历统计():
    tempStr=['学历不限','大专及以上','统招本科','本科及以上','硕士及以上','博士']
    tempNum=[]
    for i in range(len(tempStr)):
        print_name = data["学历要求"].str.contains(tempStr[i])
        number = print_name[print_name == 1].index
        tempNum.append(len(number))
    line = (
        Line()
            .add_xaxis(tempStr)
            .add_yaxis("数量", tempNum, is_connect_nones=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="学历统计"))
    )
    return line

def 公司类型统计():
    funnel = (
        Funnel()
            .add("公司类型",
            [list(z) for z in zip(data['公司信息'].value_counts().index[0:15], data['公司信息'].value_counts()[0:15].astype(int))],
            label_opts=opts.LabelOpts(position="inside")
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="公司类型统计"))
    )
    return funnel

def 每个学历的平均薪资():
    round(data['最低薪资(k)'].astype(int),2)
    salary=data.groupby(by=['学历要求'])['最低薪资(k)'].mean()
    pie = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(data['学历要求'].value_counts().index[0:6], salary[0:6])],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="每个学历的平均薪资（k）"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return pie

def 最低经历统计():
    e01 = len(data[data['最低经历(年)'] < 1])
    e2 = len(data[(data['最低经历(年)'] >= 1) & (data['最低经历(年)'] < 2)])
    e35 = len(data[(data['最低经历(年)'] >= 3) & (data['最低经历(年)'] < 5)])
    e5 = len(data[(data['最低经历(年)'] >= 5)])

    bar = (
        Bar()
            .add_xaxis(['经历不限','1~2年','3~5年','不低于5年'])
            .add_yaxis("数量", [e01, e2, e35, e5], category_gap=0,)
            .set_global_opts(title_opts=opts.TitleOpts(title="最低经历统计"))
    )
    return bar

def 数据词云1():
    words=[]
    for i in range(len(data['职位名称'].value_counts().index)):
        word=(data['职位名称'].value_counts().index[i],data['职位名称'].value_counts()[i].astype(str))
        words.append(word)
    wordcloud=(
        WordCloud()
            .add(series_name="热点分析", data_pair=words, word_size_range=[6, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return wordcloud

def 数据词云2():
    words=[]
    for i in range(len(data['公司信息'].value_counts().index)):
        word=(data['公司信息'].value_counts().index[i],data['公司信息'].value_counts()[i].astype(str))
        words.append(word)
    wordcloud=(
        WordCloud()
            .add(series_name="热点分析", data_pair=words, word_size_range=[6, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return wordcloud


def main():
    page = Page()
    page.add(每个地区的数据条目数(), 每个类别的公司数量(),学历统计(),公司类型统计(),每个学历的平均薪资(),最低经历统计(),数据词云1(),数据词云2()).render('数据可视化.html')


if __name__ == '__main__':
    main()