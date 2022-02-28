#网络小说数据爬取

import requests, time, csv
import pandas as pd
from lxml import etree
from fake_useragent import UserAgent

proxy = {
    'http': '211.65.197.93:80'
}

#获取页面的URL地址
def get_url(url):
    #创建一个存放所有url地址的数组
    all_url = []
    #获取页码数量的每一页的url地址(以下为400页)
    #1~400页已爬取完
    for i in range(401,800):
        all_url.append( url + "/l_0_" + str(i) + ".html")
    return all_url

#获取小说详细页的URL地址
def get_book_url(all_url):
    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": UserAgent().random
    }
    num = 0
    #统计页数
    for i in all_url:
        # print(i)
        r = requests.get(i , headers = headers)
        html = etree.HTML(r.text)
        url_ls = html.xpath("//div[@class='TwoBox02_08']/h1/a/@href")
        #给a标签数据加上”https:“开头
        for j in range(len(url_ls)):
            url_ls[j] = "https:" + url_ls[j]
        # print(url_ls)
        analysis_html(url_ls)
        time.sleep(1)
        print("第%s页爬完了" % i)
        num += 1

#保存HTML元素
def analysis_html(url_ls):
    for i in url_ls:
        headers = {
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": UserAgent().random
        }
        r = requests.get(i, headers=headers)
        html = etree.HTML(r.text)

        # 名称
        name = (html.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div[1]/div[1]/h1/text()"))[0]
        # print(name)
        # 总阅读数
        read = html.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div[1]/div[2]/span[3]/span/text()")[0]
        # print(read)
        # 总鲜花数
        flower = html.xpath("/html/body/div[3]/div[3]/div[1]/div[3]/text()")[0]
        # print(flower)
        # 总催更票数
        ticket_cui = html.xpath("/html/body/div[3]/div[3]/div[3]/div[3]/text()")[0]
        # print(ticket_cui)
        # 总打赏(单位万)
        reward = html.xpath("/html/body/div[3]/div[3]/div[5]/div[3]/text()")[0]
        # print(reward)
        # 总月票数
        ticket_yue = html.xpath("/html/body/div[3]/div[3]/div[7]/div[3]/text()")[0]
        # print(ticket_yue)
        # 总分享次数
        share = html.xpath("/html/body/div[3]/div[3]/div[9]/div[3]/text()")[0]
        # print(share)
        # 评分
        score = html.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div[2]/span[1]/text()")[0]
        # print(score)
        # 好评人数
        good_count = html.xpath("/html/body/div[3]/div[3]/div[10]/div[4]/span/text()")[0]
        # print(good_count)
        # 小说分类
        type = html.xpath("/html/body/div[3]/div[2]/div[5]/div[1]/div[2]/div[1]/span/span/a/text()")[0]
        # print(type)
        #保存数据
        save_data(name, read, flower, ticket_cui, reward, ticket_yue, share, score, good_count, type)


#保存数据
def save_data(name, read, flower, ticket_cui, reward, ticket_yue, share, score, good_count, type):
    result = [name] + [read] + [flower] + [ticket_cui] + [reward] + [ticket_yue] + [share] + [score] + [good_count] + [type]
    with open(r'网络小说信息数据.csv', 'a', encoding='utf_8_sig', newline="") as f:
        wt = csv.writer(f)
        wt.writerow(result)
        print('已写入')
        f.close()


if __name__ == '__main__':
    url = "https://b.faloo.com"
    # headers = {
    #     "Upgrade-Insecure-Requests": "1",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    # }
    #获取每一页的url
    all_url = get_url(url)
    #设置表头
    with open(r'网络小说信息数据.csv', 'a', encoding='utf_8_sig', newline="")as f:
        table_label = ['名称', '总阅读数', '总鲜花数', '总催更票数', '总打赏(单位万)', '总月票数', '总分享次数', '评分', '好评人数', '小说分类']
        wt = csv.writer(f)
        wt.writerow(table_label)
    #获取详细页的url
    get_book_url(all_url)
