# encoding='utf-8'
import pandas as pd
import matplotlib as mpl
import matplotlib.pylab as plt
import wordcloud
from imageio import imread


def analysis_data():
    # 显示的最大行数和列数，如果超额就显示省略号，这个指的是多少个dataFrame的列。
    # pd.set_option('display.max_rows', 30000)
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', None)
    pd.set_option("display.unicode.ambiguous_as_wide", True)  # 输出列表标签与列对齐
    pd.set_option("display.unicode.east_asian_width", True)  # 输出列表标签与列对齐

    # 读取文件
    data = pd.read_excel("../数据分析/预处理文件.xlsx")

    sorts = ["java", "python", "数据分析", "算法", "Android", "前端"]

    print("所获取信息中关于公司类型的统计".center(100, "—"))
    tempStr = ['互联网+','互联网/电商','计算机软件','电子/芯片/半导体','IT服务','通信业','人工智能','汽车/摩托车','电子商务',
               '制药/生物工程','计算机/网络设备','基金/证券/投资','医疗器械','专业服务','机械/机电/重工','互联网金融','仪器/电气/自动化',
               '企业服务软件','银行','大数据','芯片/集成电路','智能硬件','自动驾驶','快消品','交通/物流/运输','O2O服务','教育培训',
               '游戏产业','房地产/建筑','批发零售' ]
    tempNum = []
    for i in range(len(tempStr)):
        print_name = data["公司信息"].str.contains(tempStr[i])
        number = print_name[print_name == 1].index
        tempNum.append(len(number))
        print("公司类型为'{}'的共有{}个".format(tempStr[i], len(number)))

    # 解决中文乱码问题
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 10  # 设置字体大小，全局有效
    # 创建窗口,分辨率:像素/英寸
    plt.figure(figsize=(15, 5), dpi=100)
    x = []
    y = []
    for i in range(len(tempStr)):
        x.append(tempStr[i])
        y.append(tempNum[i])
    # 绘制柱状图
    plt.bar(x, y, color='#87CEFA', alpha=1, label='数目')
    plt.title('关于公司类型的统计', fontproperties='SimHei', fontsize=30, color='b')
    # plt.tick_params(axis='x', labelsize=15)  # 设置x轴标签大小
    plt.xticks(rotation=45)
    plt.xlabel('类型', fontproperties='SimHei', fontsize=20, color='y')
    plt.ylabel('岗位数量', fontdict={'name': 'SimHei', 'size': '20', 'color': 'y'})
    plt.legend()  # 显示图例
    plt.tight_layout()  # 调整整体空白
    plt.subplots_adjust(wspace=0, hspace=0)  # 调整子图间距
    # plt.show()#显示图形
    plt.savefig('关于公司类型的统计.jpg')
    print("保存成功")


if __name__ == '__main__':
    analysis_data()
