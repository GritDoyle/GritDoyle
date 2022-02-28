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
    pd.set_option('display.width',None)
    pd.set_option("display.unicode.ambiguous_as_wide", True)  # 输出列表标签与列对齐
    pd.set_option("display.unicode.east_asian_width", True)  # 输出列表标签与列对齐

    # 读取文件
    data=pd.read_excel("../数据分析/预处理文件.xlsx")

    sorts = ["java", "python", "数据分析", "算法", "Android", "前端"]

    print("所获取信息中关于学历要求统计".center(100, "—"))
    tempStr=['学历不限','大专及以上','统招本科','本科及以上','硕士及以上','博士']
    tempNum=[]
    for i in range(len(tempStr)):
        print_name = data["学历要求"].str.contains(tempStr[i])
        number = print_name[print_name == 1].index
        tempNum.append(len(number))
        print("岗位需'{}'的公司共有{}个".format(tempStr[i],len(number)))

    # 解决中文乱码问题
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus']=False
    plt.rcParams['font.size'] = 20  # 设置字体大小，全局有效
    # 创建窗口,分辨率:像素/英寸
    plt.figure(figsize=(15,5),dpi=100)
    x=[tempStr[0],tempStr[1],tempStr[2],tempStr[3],tempStr[4],tempStr[5]]
    y=[tempNum[0],tempNum[1],tempNum[2],tempNum[3],tempNum[4],tempNum[5]]
    # 绘制柱状图
    plt.bar(x,y,color='#87CEFA',alpha=1,label='数目')
    plt.title('关于学历要求的统计', fontproperties='SimHei', fontsize=30, color='b')
    # plt.tick_params(axis='x', labelsize=15)  # 设置x轴标签大小
    # plt.yticks(rotation=55)
    plt.xlabel('学历', fontproperties='SimHei', fontsize=20, color='y')
    plt.ylabel('岗位数量', fontdict={'name': 'SimHei', 'size': '20', 'color': 'y'})
    plt.legend()#显示图例
    plt.tight_layout()  # 调整整体空白
    plt.subplots_adjust(wspace=0, hspace=0)  # 调整子图间距
    # plt.show()#显示图形
    plt.savefig('关于学历要求的统计.jpg')
    print("保存成功")


if __name__ == '__main__':
    analysis_data()