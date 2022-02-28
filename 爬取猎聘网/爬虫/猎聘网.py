#coding:utf-8
import requests
import csv
import pandas as pd
import time

from bs4 import BeautifulSoup
from sqlalchemy import create_engine


def recruit(name,area,page):
    url="https://www.liepin.com/zhaopin/?headId=365c9bade58fb325cb6bb6594dc75fa8&ckId=f0e5bfb47f65cd144ff4161aa1c65be3&key=%s&dq=%s&currentPage=%d"%(name,area,page)
    # #请求的头部，User-Agent为浏览器的类型
    headers={'User-Agent':'Mozilla/5.0(Windows NT 6.1;WOW64) AppleWebKit/537.36(KHTML,like Gecko)Chrome/58.0.3029.96 Safari/537.36'}
    # requests获取html
    html = requests.get(url, headers=headers)
    # 写入文件
    with open('猎聘网.html', 'wb') as f:
        f.write(html.content)
    f.close()
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(html.content, "html.parser")
    # 解析div--class为indent的所有项table
    items = soup.find("section", class_="content-left-section").find_all("li")
    recruit_infos=[] # 存储信息
    # 遍历所有列表项
    for item in items:
        recruit_info={} # 临时存储
        recruit_info["name"]=item.find("div",class_="ellipsis-1").get("title").replace("\u2fbc","").replace("\u2f2f","").replace("\xa0","").replace("\u2f8d","").replace("\u2f45","").replace("\u2f5b","").replace("\u2fb3","").replace("\u2f83","").replace("\uf0d8","").replace("\uf06c","").replace("\u30fb","").replace("\u2f64","").replace("\u25b7","").replace("\u25c1","") if (item.find("div", "ellipsis-1")) else "" #职位名称
        recruit_info["place"]=item.find("span",class_="ellipsis-1").text if (item.find("span", "ellipsis-1")) else "" #工作地点
        recruit_info["statue"]=item.find("span",class_="job-tag").text if (item.find("span", "job-tag")) else "" #招聘状态
        recruit_info["salary"]=item.find("span",class_="job-salary").text.replace("·","-") if (item.find("span", "job-salary")) else ""#参考薪资
        recruit_info["exp"]=item.find("div",class_="job-labels-box").text.replace("\n","-") if (item.find("div", "job-labels-box")) else "" #学历经验
        recruit_info["firm"]=item.find("span",class_="company-name ellipsis-1").text.replace("\xae","") if (item.find("span", "company-name ellipsis-1")) else "" #公司名称
        recruit_info["type"]=item.find("div",class_="company-tags-box ellipsis-1").text.replace("\n","-") if (item.find("div", "company-tags-box ellipsis-1")) else "" #公司信息
        recruit_info["contacts"]=item.find("div",class_="recruiter-name ellipsis-1").text if (item.find("div", "recruiter-name ellipsis-1")) else "" #联系人
        recruit_infos.append(recruit_info)
        # print(recruit_info)
    return recruit_infos


# 进度条函数
def process_bar(percent, start_str='', end_str='', total_length=0):
    bar = ''.join(["\033[31m%s\033[0m" % '   '] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + '{:.1f}%|'.format(percent * 100) + end_str
    print(bar, end='', flush=True)
    # return bar


# 存储函数
def save_recruit_info():
    # 新建一个csv的文件
    recruit_info = open('recruit_info_total.csv', 'w', encoding='gbk', newline='')
    writer = csv.writer(recruit_info)  # CSV写入的参数为一个list
    writer.writerow(['职位名称','工作地点','招聘状态','参考薪资','学历经验','公司名称','公司信息','联系人'])
    # 爬虫获取招聘数据
    names=["java","python","数据分析","算法","Android","前端"] #,"嵌入式","运维","IOS","C++"
    areas=["010","020","060020","060080","070020","170020","050020","050090"] #北京、,"030","210040"天津、大连、上海、南京、苏州﹑杭州﹑武汉、广州、深圳、,"040","280020"重庆、成都 # 区域码  090040010思明区 090040030湖里区 090040040集美区 090040020海沧区 090040050同安区 090040060翔安区
    for name in names:
        process_bar(names.index(name) / len(names), start_str='|', end_str="100%", total_length=15)
        for area in areas:
            page = 0  # 起始页
            total_page = 9  # 总页数
            while (page <= total_page):
                time.sleep(1)  # 设置单个的爬取时间间隔为1s，避免IP被封
                infoList = recruit(name,area,page)
                # 将信息写入CSV文件中
                for item in infoList:
                    writer.writerow(
                        [item['name'], item['place'], item['statue'], item['salary'],item['exp'],item['firm'],item['type'],item['contacts']])

                page += 1  # 页数加一
    # 关闭csv文件
    recruit_info.close()
    # 创建MySQL数据库连接
    data = pd.read_csv(open("recruit_info_total.csv", encoding="gbk"), sep=',', header=0)
    # 小数据清洗
    data = data.fillna("")
    data = data[data['职位名称'] != ""]
    print(data)
    # engine = create_engine("mysql+pymysql://root:@localhost:3306/studyfiles?charset=utf8")
    # data.to_sql('猎聘网_all',engine,index=True)
    # print('成功存入数据库!')


if __name__ == '__main__':
    save_recruit_info()