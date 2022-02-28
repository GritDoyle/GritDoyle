import re
import csv
import time
import requests
from bs4 import BeautifulSoup


# 电影爬虫函数
def get_movies(start):
    url = "https://movie.douban.com/top250?start=%d&filter=" % start
    lists = []
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, "html.parser")
    items = soup.find("ol", class_="grid_view").find_all("li")
    for i in items:
        movie = {}
        movie["rank"] = i.find("em").text
        # movie["link"] = i.find("div", "pic").find("a").get("href")
        movie["name"] = i.find("span", "title").text
        movie["director"] = re.findall(r"导演: (.+?) ",
                                       re.findall(re.compile(r'<p class="">(.*?)<br/>', re.S), str(i))[0].replace(
                                           "\n                            ", "").replace("\xa0", "").replace("\xf4",""))[0]
        movie["score"] = i.find("span", "rating_num").text  # 评分
        movie["score_num"] = re.findall(re.compile(r'<span>(.+?)人评价', re.S), str(i))[0]  # 评分人数
        movie["quote"] = i.find("span", "inq").text if (i.find("span", "inq")) else ""  # 箴言
        lists.append(movie)
    return lists


# 进度条函数
def process_bar(percent, start_str='', end_str='', total_length=0):
    bar = ''.join(["\033[31m%s\033[0m" % '   '] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent * 100) + end_str
    print(bar, end='', flush=True)


if __name__ == '__main__':
    # 新建一个csv的文件
    movies = open('豆瓣TOP250.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(movies)  # CVS写入的参数为一个list
    writer.writerow(['rank', 'name', 'director', 'score', 'score_num', 'quote'])

    # 爬虫获取电影数据
    page = 0  # 其实页数
    pageN = 250  # 信息总数
    end_str = '100%'
    while (page < pageN):
        time.sleep(1)  # 设置单个电影页面的爬取时间间隔为1s，避免IP被封
        movieList = get_movies(page)
        # 将电影信息写入CSV文件中
        for item in movieList:
            writer.writerow(
                [item['rank'], item['name'], item['director'], item['score'], item['score_num'],
                 item['quote']])

        page += 25  # 每页25个电影数据
        process_bar(page / pageN, start_str='', end_str=end_str, total_length=15)

    # 关闭csv文件
    movies.close()
