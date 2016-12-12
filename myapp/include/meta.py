#!/bin/env python
#-*-coding:utf-8-*-
import MySQLdb,sys,string,time,datetime
from django.contrib.auth.models import User
from myapp.include import function as func
from multiprocessing import Process
from myapp.models import Db_name,Db_account,Db_instance,Oper_log,Task,Incep_error_log

public_user = func.public_user

def mysql_query(sql,user,passwd,host,port,dbname):
    try:
        conn=MySQLdb.connect(host=host,user=user,passwd=passwd,port=int(port),connect_timeout=5,charset='utf8')
        conn.select_db(dbname)
        cursor = conn.cursor()
        count=cursor.execute(sql)
        index=cursor.description
        col=[]
        #get column name
        for i in index:
            col.append(i[0])
        result=cursor.fetchall()
        # result=cursor.fetchmany(size=int(limitnum))
        cursor.close()
        conn.close()
        return (result,col)
    except Exception,e:
        return([str(e)],''),['error']

def get_metadata(hosttag,flag,tbname=''):
    dbname = Db_name.objects.get(dbtag=hosttag).dbname
    #get table list
    if flag ==1:
        if len(tbname)>0:
            sql = "select TABLE_NAME,TABLE_TYPE,ENGINE,TABLE_COLLATION,TABLE_COMMENT from information_schema.tables where table_schema='"+dbname+"'" +" and TABLE_NAME like '%"+tbname+"%'"
        else :
            sql = "select TABLE_NAME,TABLE_TYPE,ENGINE,TABLE_COLLATION,TABLE_COMMENT from information_schema.tables where table_schema='"+dbname+"'"
        results, col, tar_dbname = get_data(hosttag,sql)
        return results,col,tar_dbname
    #get column list
    elif flag==2:
        sql = "SELECT ORDINAL_POSITION AS POS,COLUMN_NAME,COLUMN_TYPE,COLUMN_DEFAULT,IS_NULLABLE,CHARACTER_SET_NAME,COLLATION_NAME,COLUMN_KEY,EXTRA,COLUMN_COMMENT FROM information_schema.COLUMNS  where TABLE_SCHEMA='"+dbname+"'"+" and TABLE_NAME='"+tbname+"'"+' ORDER BY POS'
        results, col, tar_dbname = get_data(hosttag, sql)
        return results, col, tar_dbname
    #get indexes list
    elif flag==3:
        sql = "SELECT INDEX_NAME,NON_UNIQUE,SEQ_IN_INDEX,COLUMN_NAME,COLLATION,CARDINALITY,SUB_PART,PACKED,NULLABLE,INDEX_TYPE,COMMENT,INDEX_COMMENT FROM information_schema.statistics  where TABLE_SCHEMA='"+dbname+"'"+" and TABLE_NAME='"+tbname+"'"
        results, col, tar_dbname = get_data(hosttag, sql)
        return results, col, tar_dbname
    #table details
    elif flag == 4:
        sql = "select * from information_schema.tables where TABLE_SCHEMA='"+dbname+"'"+" and TABLE_NAME='"+tbname+"'"
        results, col, tar_dbname = get_data(hosttag, sql)
        return results, col, tar_dbname

def get_data(hosttag,sql):
    a = Db_name.objects.filter(dbtag=hosttag)[0]
    #a = Db_name.objects.get(dbtag=hosttag)
    tar_dbname = a.dbname
    #如果instance中有备库role='read'，则选择从备库读取
    try:
        if a.instance.all().filter(role='read')[0]:
            tar_host = a.instance.all().filter(role='read')[0].ip
            tar_port = a.instance.all().filter(role='read')[0].port
    #如果没有设置或没有role=read，则选择第一个读到的实例读取
    except Exception,e:
        tar_host = a.instance.all()[0].ip
        tar_port = a.instance.all()[0].port

    for i in a.db_account_set.all():
        if i.role == 'admin':
            tar_username = i.user
            tar_passwd = i.passwd
            break
    #print tar_port+tar_passwd+tar_username+tar_host
    try:
        results,col = mysql_query(sql,tar_username,tar_passwd,tar_host,tar_port,tar_dbname)
    except Exception, e:
        #防止失败，返回一个wrong_message
        results,col = ([str(e)],''),['error']
        #results,col = mysql_query(wrong_msg,user,passwd,host,int(port),dbname)
    return results,col,tar_dbname