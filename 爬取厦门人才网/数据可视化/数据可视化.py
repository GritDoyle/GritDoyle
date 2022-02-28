import pandas as pd
from pyecharts.charts import Bar, Page, Pie, Line, WordCloud
from pyecharts import options as opts

pd.set_option('display.max_rows', 30000)
data=pd.read_excel("../数据分析/预处理文件.xlsx")

nav=['职位名称','公司名称','工作地点','学历','日期']
for i in range(len(nav)):
    print(data['{}'.format(nav[i])].value_counts(),'\n')

def 职位数量统计():
    data['职位名称'].value_counts()
    bar = Bar()
    x,y=[],[]
    for i in range(len(data['职位名称'].value_counts().index[0:50])):
        x.append(data['职位名称'].value_counts().index[i])
        y.append(int(data['职位名称'].value_counts()[i]))
    bar.add_xaxis(x)
    bar.add_yaxis("数量",y)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="职位数量统计"))
    return bar

def 公司招聘数量():
    data['公司名称'].value_counts()
    bar = Bar()
    x, y = [], []
    for i in range(len(data['公司名称'].value_counts().index[0:50])):
        x.append(data['公司名称'].value_counts().index[i])
        y.append(int(data['公司名称'].value_counts()[i]))
    bar.add_xaxis(x)
    bar.add_yaxis("数量", y)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="公司招聘数量统计"))
    return bar

def 工作地点统计():
    tempStr = data['工作地点'].value_counts().index.tolist()[0:30]
    tempNum = []
    for i in range(len(tempStr)):
        print_name = data["工作地点"].str.contains(tempStr[i])
        number = print_name[print_name == 1].index
        tempNum.append(len(number))
    line = (
        Line()
            .add_xaxis(tempStr)
            .add_yaxis("数量", tempNum, is_connect_nones=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="工作地点统计"))
    )
    return line

def 学历统计():
    pie = (
        Pie()
            .add("", [list(z) for z in zip(data['学历'].value_counts().index, data['学历'].value_counts())])
            .set_global_opts(title_opts=opts.TitleOpts(title="学历统计"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return pie

def 每个学历的最低平均薪资():
    round(data['最低月薪'].astype(int),2)
    salary=data.groupby(by=['学历'])['最低月薪'].mean()
    pie = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(data['学历'].value_counts().index, salary)],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="每个学历的最低平均薪资（k）"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return pie

def 每个学历的最高平均薪资():
    round(data['最高月薪'].astype(int),2)
    salary=data.groupby(by=['学历'])['最高月薪'].mean()
    pie = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(data['学历'].value_counts().index, salary)],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="每个学历的最高平均薪资（k）"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return pie

def 数据词云1():
    words=[]
    for i in range(len(data['公司名称'].value_counts().index)):
        word=(data['公司名称'].value_counts().index[i],data['职位名称'].value_counts()[i].astype(str))
        words.append(word)
    wordcloud=(
        WordCloud()
            .add(series_name="公司热点分析", data_pair=words, word_size_range=[6, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="公司热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return wordcloud
#
def 数据词云2():
    words=[]
    for i in range(len(data['职位名称'].value_counts().index)):
        word=(data['职位名称'].value_counts().index[i],data['职位名称'].value_counts()[i].astype(str))
        words.append(word)
    wordcloud=(
        WordCloud()
            .add(series_name="职位热点分析", data_pair=words, word_size_range=[6, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="职位热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return wordcloud

def 数据词云3():
    words=[]
    for i in range(len(data['工作地点'].value_counts().index)):
        word=(data['工作地点'].value_counts().index[i],data['工作地点'].value_counts()[i].astype(str))
        words.append(word)
    wordcloud=(
        WordCloud()
            .add(series_name="工作地点热点分析", data_pair=words, word_size_range=[6, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="工作地点热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return wordcloud


def main():
    page = Page()
    page.add(职位数量统计(), 公司招聘数量(),工作地点统计(),学历统计(),每个学历的最低平均薪资(),每个学历的最高平均薪资(),数据词云1(),数据词云2(),数据词云3()).render('数据可视化.html')


if __name__ == '__main__':
    main()