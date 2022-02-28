import re
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from requests_html import HTMLSession


# 招聘网爬虫函数
def recruit(page):
    recruit_infos = [] #临时存储信息
    total_info = [] #存储总信息
    session = HTMLSession()
    r = session.get(
        'https://www.xmrc.com.cn/net/info/Resultg.aspx?a=a&g=g&recordtype=1&searchtype=3&keyword=项目经理&releasetime=365&worklengthflag=0&jobtype=9902&sortby=updatetime&ascdesc=Desc&pagesize=20&PageIndex=%d'%page
    )
    r.html.render() #渲染爬取动态页面
    # 写入文件
    with open('爬虫/厦门人才招聘网.html', 'wb') as f:
        f.write(r.content)
    f.close()
    # CSS选择器获取信息
    recruit_info = r.html.find(
        '#ctl00\$Body\$JobRepeaterPro_main_div > table.text-center.queryRecruitTable > tbody > tr:nth-child(n) > td:nth-child(n) > a')
    recruit_infos += recruit_info
    for i in range(0,len(recruit_infos),7):
        recruits = {}  # 临时存储
        recruits["name"] = recruit_infos[i].text.replace("\n","") # 职位名称
        recruits["firm"] = recruit_infos[i+1].text  # 公司名称
        recruits["place"] = recruit_infos[i+2].text  # 工作地点
        recruits["salary"] = recruit_infos[i+3].text.replace("\n","")  # 参考月薪
        recruits["edu"] = recruit_infos[i+4].text  # 学历
        recruits["time"] =  recruit_infos[i+5].text # 发布时间
        total_info.append(recruits)
        print(recruits)
    return total_info


# 进度条函数
def process_bar(percent, start_str='', end_str='', total_length=0):
    bar = ''.join(["\033[31m%s\033[0m" % '   '] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:.1f}%|'.format(percent * 100) + end_str
    print(bar, end='', flush=True)


# 存储函数
def save_recruit_info():
    # 新建一个csv的文件
    recruit_info = open('爬取厦门人才网/recruit_info_project.csv', 'w', encoding='gbk', newline='')
    writer = csv.writer(recruit_info)  # CSV写入的参数为一个list
    writer.writerow(['职位名称','公司名称','工作地点','参考月薪','学历','发布时间'])
    # 爬虫获取招聘数据
    page = 1  # 起始页
    total_page = 5  # 总页数
    while (page <= total_page):
        time.sleep(1)  # 设置单个的爬取时间间隔为1s，避免IP被封
        infoList = recruit(page)
        # 将图书信息写入CSV文件中
        for item in infoList:
            writer.writerow(
                [item['name'], item['firm'], item['place'], item['salary'],item['edu'],item['time']])
        page += 1  # 页数加一
        process_bar(page/total_page, start_str='|', end_str="100%", total_length=10)
    # 关闭csv文件
    recruit_info.close()
    # 创建MySQL数据库连接
    data = pd.read_csv(open("爬取厦门人才网/recruit_info_project.csv", encoding="gbk"), sep=',', header=0)
    print(data)
    engine = create_engine("mysql+pymysql://root:@localhost:3306/studyfiles?charset=utf8")
    data.to_sql('厦门人才网_project',engine,index=True)
    print('成功存入数据库!')


if __name__ == '__main__':
    save_recruit_info()
