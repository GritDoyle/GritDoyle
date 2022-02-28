import json
import re
import csv
import time
import requests
from bs4 import BeautifulSoup


# 进度条函数
def process_bar(percent, start_str='', end_str='', total_length=0):
    bar = ''.join(["\033[31m%s\033[0m" % '   '] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent * 100) + end_str
    print(bar, end='', flush=True)


# 爬取1000部电影豆瓣评论数据
def get_comment(start):
    # 定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74',
        'Cookie': 'gr_user_id=98308e02-8db9-49e0-9de4-890c4c193f72; douban-fav-remind=1; bid=lYZXRcdtPCQ; ll="118207"; __yadk_uid=MGOgDm06nYw04PGytvJV0PNz7fcjjjxW; _vwo_uuid_v2=DBE539F6D5A0AAC548649716B46A4BA99|49c97020fdcd5f5fe11c41cfe53d55a9; dbcl2="232174515:5qd1Rlp+aN0"; push_noty_num=0; push_doumail_num=0; __gads=ID=6d5847587dd580b5-22a70fbac3c50046:T=1611246947:S=ALNI_MaZgTkwWDcO95Mg44vDx6pLbT645A; __utmv=30149280.23217; ck=SYr0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1613784142%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.304848869.1568545867.1613747595.1613784142.30; __utmc=30149280; __utmz=30149280.1613784142.30.5.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1213419331.1572768031.1613747595.1613784142.21; __utmb=223695111.0.10.1613784142; __utmc=223695111; __utmz=223695111.1613784142.21.5.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=30149280.2.10.1613784142; _pk_id.100001.4cf6=dbfcd1ce15eefbd7.1572768031.20.1613785461.1613750844.'}
    movieItem_baseUrl = "https://movie.douban.com/subject/"
    baseUrl = "https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={}".format(
        start)  # 爬取电影页面
    movie_ids = []
    response = requests.get(baseUrl, headers=headers)
    # 写入文件
    with open('豆瓣电影排行榜.html', 'wb') as f:
        f.write(response.content)
    f.close()
    soup = BeautifulSoup(response.text , 'lxml')
    singlePage_jsonList = soup.find('p').text # 返回的response为json字符串
    # 将一个JSON编码的字符串转换回一个Python数据结构字典
    json_str = json.loads(singlePage_jsonList)['data']
    json_str_list = list(json_str)

    for item in json_str_list:  # 获取每页20个电影的ID
        movie_ids.append(item['id'])

    lists = []  # 以列表形式存放数据

    for id in movie_ids:  # 获取每页20个电影信息
        dataCount = 0  # 获取数据的个数
        while dataCount < 40:  # 爬取40条评论
            time.sleep(1.5)  # 设置单个电影页面的爬取时间间隔为1s，避免IP被封
            movie_url = movieItem_baseUrl + str(id) + '/comments?start={}&limit=20&status=P&sort=new_score'.format(
                dataCount)
            movie_response = requests.get(movie_url, headers=headers)
            movie_soup = BeautifulSoup(movie_response.text, "html.parser")
            comment_list = movie_soup.find_all(
                'div', class_='comment')  # 获取单个电影的各页评论列表
            for item in comment_list:
                movie = {}
                movie['电影名称'] = movie_soup.find(id="content").h1.get_text()[
                                0:-2]  # 获取电影标题
                try:
                    movie['用户名'] = re.findall(re.compile(r'\n(.+?)\n', re.S), item.find(
                        'span', class_='comment-info').get_text())[0]  # 获取用户名称
                except:
                    movie['用户名'] = ""
                try:
                    movie['评论内容'] = item.find(
                        'span', class_='short').get_text()  # 获取评论实体
                except:
                    movie['评论内容'] = ""
                try:
                    movie['评论星级'] = \
                        item.find('span', class_='comment-info').find('span', {'class': re.compile("allstar")}).get(
                            'class')[0][-2:-1]  # 获取评论星级
                except:
                    movie['评论星级'] = ""
                try:
                    movie['评论点赞数'] = item.find(
                        'span', class_='votes').get_text()  # 获取评论点赞数
                except:
                    movie['评论点赞数'] = ""
                lists.append(movie)
            dataCount += 20
    return lists


if __name__ == '__main__':
    # 新建一个csv的文件
    movies = open('豆瓣华语电影.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(movies)  # CVS写入的参数为一个list
    writer.writerow(['电影名称', '用户名', '评论内容', '评论星级', '评论点赞数'])

    # 爬虫获取电影数据
    pageStart = 600  # 起始页数
    pageN = 100  # 信息总数
    page = 0 # 页面个数
    end_str = '100%'
    print("下载进度条：")
    process_bar(0, start_str='', end_str=end_str, total_length=15)
    while page < pageN:
        commentList = get_comment(pageStart)
        # 将电影信息写入CSV文件中
        for item in commentList:
            writer.writerow(
                [item['电影名称'], item['用户名'], item['评论内容'], item['评论星级'], item['评论点赞数']])
        pageStart += 20  # 每页20个电影数据
        page += 20 # 计数+20
        process_bar(page / pageN, start_str='', end_str=end_str, total_length=15)

    # 关闭csv文件
    movies.close()
    print("\nDone!")
