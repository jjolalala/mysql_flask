import pymysql
from flask import Flask
import random

app = Flask(__name__)

db = pymysql.connect(host='localhost', user='root', password='1111111111', port=3306, db='sql')
cursor = db.cursor()
table = 'overview'
sql = 'SELECT * FROM overview'
cursor.execute(sql)
# 获取所有记录列表
# results = cursor.fetchall()


@app.route('/')
def index():
    data = get_data()
    if data:
        return f'<h1>{data}</h1>'
    else:
        return f'<h1>数据到底啦</h1>'


def get_data():
    try:
        row = cursor.fetchone()
        # row = random.choice(results)
        return row
    except:
        print('Error')


if __name__ == '__main__':
    app.run(debug=True)