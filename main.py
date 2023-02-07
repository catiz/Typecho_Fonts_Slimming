import re
import os
import pymysql
import pandas as pd
import sys
from fontTools.subset import main as ss
from fontTools.ttLib import TTFont


class MysqlSave:

    def __init__(self):
        self.content = pymysql.Connect(
            host='172.1.2.255',
            port=3306,
            user='user',
            password='password',
            database='typecho',
            charset='utf8',  # 使用字符集
        )
        self.cursor = self.content.cursor()

    def search_and_save(self, sql, csv_file):
        self.cursor.execute(sql)

        des = self.cursor.description
        title = [each[0] for each in des]

        result_list = []
        for each in self.cursor.fetchall():
            result_list.append(list(each))

        df_dealed = pd.DataFrame(result_list, columns=title)
        df_dealed.to_csv(csv_file, index=None, encoding='utf_8_sig')


def go(path):
    f = open(path, "r", encoding='utf-8')
    print(path)
    data = f.readlines()
    f.close()

    for line in data:
        regular = re.findall('[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]',
                             line)
        str1 = "".join(regular)
        f1 = open("ss.txt", "a+", encoding='utf-8')
        f1.writelines(str1)

        f1.close()


if __name__ == '__main__':
    mysql = MysqlSave()
    mysql.search_and_save('SELECT * FROM typecho_comments', './sql/typecho_comments.csv')
    mysql.search_and_save('SELECT * FROM typecho_contents', './sql/typecho_contents.csv')
    mysql.search_and_save('SELECT * FROM typecho_metas', './sql/typecho_metas.csv')
    mysql.search_and_save('SELECT * FROM typecho_options', './sql/typecho_options.csv')
    mysql.search_and_save('SELECT * FROM typecho_users', './sql/typecho_users.csv')

    sql_list = os.listdir('./sql/')
    for paths in sql_list:
        go("./sql/" + paths)

    sys.argv = [None, 'PingFang_Bold.ttf', '--text-file=./ss.txt']
    ss()
    f = TTFont('PingFang_Bold.subset.ttf')
    f.flavor = 'woff2'
    f.save('PingFang_Bold.woff2')
    os.remove("ss.txt")
