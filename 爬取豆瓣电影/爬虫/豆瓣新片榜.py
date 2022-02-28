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
    items = soup.find("div", class_="indent").find_all('table')
    movies=[]
    # 遍历所有列表项
    for item in items:
        movie={} #临时存储
        # 电影名
        try:
            movie['name'] = item.find('a', class_='nbg').get("title")
        except:
            movie['name'] = ""
        # 上映时间
        try:
            movie['time'] = item.find('p', class_='pl').get_text().split(" / ")[0]
        except:
            movie['time'] = ""
        # 电影分数
        try:
            movie['score'] = item.find('span', class_='rating_nums').get_text()
        except:
            movie['score'] = ""
        # 电影评论数
        try:
            movie['comment'] = item.find('span', class_='pl').get_text()
        except:
            movie['comment'] = ""
        movies.append(movie)
        # print(movie)
    return movies

def save_douban():
    # 新建一个csv文件
    movie=open('豆瓣新片榜.csv','w',encoding='utf-8',newline='')
    writer = csv.writer(movie)  # CSV写入的参数为一个list
    writer.writerow(['电影名称', '上映时间', '评分', '评价数'])
    page=1
    while page==1:
        time.sleep(1)  # 设置单个的爬取时间间隔为1s，避免IP被封
        items=douban()
        # 将信息写入CSV文件中
        for item in items:
            writer.writerow(
                [item['name'], item['time'], item['score'], item['comment']])
        print("爬取第{}页完毕".format(page))
        page+=1
    # 关闭csv文件
    movie.close()

if __name__ == '__main__':
    save_douban()