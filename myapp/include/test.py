#!/bin/env python
#-*-coding:utf-8-*-
import MySQLdb,sys,string,time,datetime


reload(sys)
sys.setdefaultencoding('utf8')
import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.message import Message
from email.header import Header

def get_item(data_dict,item):
    try:
       item_value = data_dict[item]
       return item_value
    except:
       return '-1'

def get_config(group,config_name):
    config = ConfigParser.ConfigParser()
    #config.readfp(open('./myapp/etc/config.ini','r'))
    config.readfp(open('../etc/config.ini','r'))
    config_value=config.get(group,config_name).strip(' ').strip('\'').strip('\"')
    return config_value

def filters(data):
    return data.strip(' ').strip('\n').strip('\br')

host = get_config('settings','host')
port = get_config('settings','port')
user = 'test'
passwd = 'test'
dbname = 'test'

def mysql_exec(sql,param):
    try:
        conn=MySQLdb.connect(host=host,user=user,passwd=passwd,port=int(port),connect_timeout=5,charset='utf8')
        conn.select_db(dbname)
        curs = conn.cursor()
        if param <> '':
            curs.execute(sql,param)
        else:
            curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()
    except Exception,e:
       print "mysql execute: " + str(e)

def check_mysql_query(sqltext,user,type='select'):
    num='1000'

    limit = ' limit '+str(num)

    sqltext = sqltext.strip()
    sqltype = sqltext.split()[0].lower()
    list_type = ['select','show','desc','explain']
    #flag 1位有效 0为list_type中的无效值
    flag=0
    while True:
        sqltext = sqltext.strip()
        lastletter = sqltext[len(sqltext)-1]
        if (not cmp(lastletter,';')):
            sqltext = sqltext[:-1]
        else:
            break
    #判断语句中是否已经存在limit，has_limit 为0时说明原来语句中是有limit的
    has_limit = cmp(sqltext.split()[-2].lower(),'limit')
    for i in list_type:
        if (not cmp(i,sqltype)):
            flag=1
            break
    if (flag==1):
        if (sqltype =='select' and has_limit!=0):
            return sqltext+limit,num
        elif (sqltype =='select' and has_limit==0):
            if (int(sqltext.split()[-1])<=int(num)):
                return sqltext,num
            else:
                tempsql=''
                numlimit=sqltext.split()[-1]
                for i in sqltext.split()[0:-1]:
                    tempsql=tempsql+i+' '
                return tempsql+num,num
        else:
            return sqltext,num
    else:
        return 'wrong',num

def main():
    result,num=check_mysql_query('select * from mysql limit 3000',user,type='select')
    print result
    print num
if __name__=='__main__':
    main()