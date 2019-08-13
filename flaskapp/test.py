import pymysql

conn = pymysql.connect(host='localhost',
        user='root',
        password='r!',
        db='mytown_project',
        charset='utf8')

try:
    with conn.cursor() as cursor:
        sql = 'SELECT f.card_image, t.title, t.location FROM Town_record t inner join File_address f on t.id = f.id order by t.id desc'
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        # (1, 'test@test.com', 'my-passwd')
finally:
    conn.close()

# -------------------------------------------------------------------

import os 
import sys
from pprint import pprint

# os.environ['Path']

# os.environ['EMAIL_PASSWORD']

print(os.environ['NO_PROXY'])
print(os.environ['EMAIL_USER'])

