import MySQLdb as mysql
import time
import random


db = 'buxs_BE_test'
username = 'deno101'
password = 'denniz'
host = '127.0.0.1'
item = [
    'Nike airs',
    'mosquito Nets',
    'Techno spark 4',
    'Sony Blender',
    'Blender 4',
    'Nike airs',
    'Nike airs',
    'Nike airs',
    'Nike airs',
    'Nike airs',
]


def connect():
    conn = mysql.connect(host, username, password, db)
    cursor = conn.cursor()

    i = 1
    for x in item:
        id = str(i)
        name = x
        price = random.randint(100, 1000)
        date_epoch = str(time.time())
        image_url = f'{i}.jpg'
        query = f"INSERT INTO buxsbackend_marketplaceproducts VALUES('{id}','{name}','{price}','{date_epoch}','all','{image_url}')"
        cursor.execute(query)
        i += 1
        conn.commit()


connect()
