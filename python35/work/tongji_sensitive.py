# coding=utf8

import pymysql

mysql_host='yuedu.activity.rds.sogou'
mysql_db='yuedu_activity'
mysql_user='copyrightupdate'
mysql_passwd='copyright1q2w3e4r'
mysql_port=3306
mysql_charset='utf8'


conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db, port=mysql_port, charset=mysql_charset)
conn.ping(True)
cur = conn.cursor()
sql = ''
