from scrapy import Selector
import requests
import os
import re
import pymysql
from pymysql.err import IntegrityError

url = 'https://movie.douban.com/subject/26425063/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def crawl():
    # 创建文件夹
    if not os.path.exists('file'):
        os.mkdir('file')

    # 爬取网页
    collect = {}

    res = requests.get(url=url, headers=headers)
    selector = Selector(text=res.text)
    title = selector.xpath('//div[@class="related-info"]/h2/i/text()').extract()
    title = re.sub(r'\n+\s+', '', ''.join(title))
    overview = selector.xpath('//div[@class="indent"]/span/text()').extract_first().strip()
    collect.update({title: overview})
    return collect


def save_to_sql(data):
    db = pymysql.connect(host='localhost', user='root', password='1111111111', port=3306, db='sql')
    cursor = db.cursor()
    table = 'overview'
    sql1 = f'CREATE TABLE IF NOT EXISTS {table} (name VARCHAR(255) NOT NULL ,' \
           f'introduction VARCHAR(255) NOT NULL, PRIMARY KEY (name))'
    try:
        cursor.execute(sql1)
    except:
        print('创建失败')
    for keys, values in data.items():
        print(keys, values)
        sql2 = f'INSERT INTO {table}(name,introduction) VALUES(%s,%s)'
        try:
            if cursor.execute(sql2, (keys, values)):
                print('插入成功')
        except IntegrityError:
            print('重复插入了')
        except:
            print('Fail')
            db.rollback()
    db.commit()


if __name__ == '__main__':
    # data = crawl()
    save_to_sql({'啦啦啦':'一只小狗'})
