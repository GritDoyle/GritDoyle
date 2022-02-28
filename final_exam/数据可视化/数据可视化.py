import pandas as pd
from pyecharts.charts import Page, Pie, Line, Funnel, WordCloud, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType

raw_data=pd.read_excel("../数据清洗/预处理文件.xlsx")

def classify_novel():
    pie = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(raw_data['小说分类'].value_counts().index,raw_data['小说分类'].value_counts())],
            center=["50%", "50%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="小说分类",pos_bottom=0,pos_left='center'),
            legend_opts=opts.LegendOpts(pos_left="0"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return pie

def total_read_top10():
    x_data = raw_data.sort_values(by=['总阅读数'], ascending=False)['名称'][0:10].tolist()
    y_data = raw_data.sort_values(by=['总阅读数'],ascending=False)['总阅读数'][0:10].tolist()

    data = [[x_data[i], y_data[i]] for i in range(len(x_data))]

    funnel=(
        Funnel(init_opts=opts.InitOpts(width="600px", height="600px"))
            .add(
            series_name="",
            data_pair=data,
            gap=2,
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%"),
            label_opts=opts.LabelOpts(is_show=True, position="inside"),
            itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=1),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="总阅读数top10",pos_bottom=30,pos_left='center'))
    )
    return funnel

def total_flowers_top10():
    bar = (
        Bar()
            .add_xaxis(raw_data.sort_values(by=['总鲜花数'], ascending=False)['名称'][0:10].tolist())
            .add_yaxis("鲜花数", raw_data.sort_values(by=['总鲜花数'],ascending=False)['总鲜花数'][0:10].tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title="总鲜花数top10", subtitle="小说排行"))
    )
    return bar

def total_share():
    y = raw_data.sort_values(by=['总分享次数'], ascending=False)['总分享次数'][0:10].tolist()
    line = (
        Line()
            .add_xaxis(raw_data.sort_values(by=['总分享次数'], ascending=False)['名称'][0:10].tolist())
            .add_yaxis("分享次数", y, is_connect_nones=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="分享次数top10",pos_bottom=0,pos_left='center'))
    )
    return line

def praise_num_top10():
    bar = (
        Bar({"theme": ThemeType.MACARONS})
            .add_xaxis(raw_data.sort_values(by=['好评人数'], ascending=False)['名称'][0:10].tolist())
            .add_yaxis("人数", raw_data.sort_values(by=['好评人数'], ascending=False)['好评人数'][0:10].tolist())
            .set_global_opts(
            title_opts={"text": "好评人数top10", "subtext": "小说排行"}
        )
    )
    return bar

def statistics():
    bar = (
        Bar()
            .add_xaxis(raw_data.groupby(['小说分类']).mean().index.tolist())
            .add_yaxis("总阅读数", raw_data.groupby(['小说分类']).mean()['总阅读数'].tolist(), stack="stack1")
            .add_yaxis("总鲜花数", raw_data.groupby(['小说分类']).mean()['总鲜花数'].tolist(), stack="stack1")
            .add_yaxis("总催更票数", raw_data.groupby(['小说分类']).mean()['总催更票数'].tolist(), stack="stack1")
            .add_yaxis("总打赏(单位万)", raw_data.groupby(['小说分类']).mean()['总打赏(单位万)'].tolist(), stack="stack1")
            .add_yaxis("总月票数", raw_data.groupby(['小说分类']).mean()['总月票数'].tolist(), stack="stack1")
            .add_yaxis("总分享次数", raw_data.groupby(['小说分类']).mean()['总分享次数'].tolist(), stack="stack1")
            .add_yaxis("好评人数", raw_data.groupby(['小说分类']).mean()['好评人数'].tolist(), stack="stack1")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="小说类型平均值统计",pos_bottom=0,pos_left='center'))
    )
    return bar

def wordcloud():
    words = []
    for i in range(len(raw_data['名称'].value_counts().index)):
        word=(raw_data['名称'].value_counts().index[i],raw_data['名称'].value_counts()[i].astype(str))
        words.append(word)
    wordcloud = (
        WordCloud()
            .add("", words, word_size_range=[20, 100])
            .set_global_opts(title_opts=opts.TitleOpts(title="小说词云",pos_bottom=0,pos_left='center'))
    )
    return wordcloud

if __name__ == '__main__':
    page = Page()
    page.add(classify_novel(),total_read_top10(),total_flowers_top10(),total_share(),praise_num_top10(),statistics(),wordcloud()).render('数据可视化.html')

