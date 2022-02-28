import csv
import time

import requests
from bs4 import BeautifulSoup


def douban():
    url='https://movie.douban.com/chart'
    # 请求的头部，User-Agent为浏览器的类型
    headers={'User-Agent':'Mozilla/5.0(Windows NT 6.1;WOW64) AppleWebKit/537.36(KHTML,like Gecko)Chrome/58.0.3029.96 Safari/537.36'}
    # requests获取html
    html = requests.get(url, headers=headers)
    # 写入文件
    with open('豆瓣电影排行榜.html', 'wb') as f:
        f.write(html.content)
    f.close()
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(html.content, "html.parser")
    items = soup.find("ul", class_="content").find_all('li')
    movies=[]
    # 遍历所有列表项
    for item in items:
        movie={} #临时存储
        # 电影名
        try:
            movie['电影名'] = item.find('div', class_='name').get_text()
        except:
            movie['电影名'] = ""
        # 波动排名
        try:
            movie['波动排名'] = '上升'+item.find('div', class_='up').get_text()
        except:
            movie['波动排名'] = '下降'+item.find('div', class_='down').get_text()
        # 现排名
        try:
            movie['现排名'] = item.find('div', class_='no').get_text()
        except:
            movie['现排名'] = ""
        movies.append(movie)
    # print(movie)
    return movies

def save_douban():
    # 新建一个csv文件
    movie=open('一周口碑榜（12月3日更新）.csv','w',encoding='utf-8',newline='')
    writer = csv.writer(movie)  # CSV写入的参数为一个list
    writer.writerow(['电影名', '波动排名', '现排名'])
    page=1
    while page==1:
        time.sleep(1)  # 设置单个的爬取时间间隔为1s，避免IP被封
        items=douban()
        # 将信息写入CSV文件中
        for item in items:
            writer.writerow(
                [item['电影名'], item['波动排名'], item['现排名']])
        print("爬取第{}页完毕".format(page))
        page+=1
    # 关闭csv文件
    movie.close()

if __name__ == '__main__':
    save_douban()