import MySQLdb,sys,string,time,datetime
from django.contrib.auth.models import User
from myapp.include import function as func
from myapp.models import Db_name,Db_account,Db_instance,Oper_log
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
    config.readfp(open('./myapp/etc/config.ini','r'))
    #config.readfp(open('../etc/config.ini','r'))
    config_value=config.get(group,config_name).strip(' ').strip('\'').strip('\"')
    return config_value

def filters(data):
    return data.strip(' ').strip('\n').strip('\br')

host = get_config('settings','host')
port = get_config('settings','port')
user = get_config('settings','user')
passwd = get_config('settings','passwd')
dbname = get_config('settings','dbname')
wrong_msg = get_config('settings','wrong_msg')

def incep_exec(sqltext,myuser,mypasswd,myhost,myport,mydbname):
    myuser=myuser.encode('utf8')
    mypasswd = mypasswd.encode('utf8')
    myhost=myhost.encode('utf8')
    myport=int(myport)
    mydbname=mydbname.encode('utf8')
    sql1="/*--user=%s;--password=%s;--host=%s;--enable-check;--port=%d;*/\
            inception_magic_start;\
            use %s;"% (myuser,mypasswd,myhost,myport,mydbname)
    sql2='inception_magic_commit;'
    sql = sql1 + sqltext + sql2
    try:
        conn=MySQLdb.connect(host='10.1.70.222',user='',passwd='',db='',port=6669,use_unicode=True, charset="utf8")
        cur=conn.cursor()
        ret=cur.execute(sql)
        result=cur.fetchall()
        #num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        #print field_names
        #for row in result:
        #    print row[0], "|",row[1],"|",row[2],"|",row[3],"|",row[4],"|",row[5],"|",row[6],"|",row[7],"|",row[8],"|",row[9],"|",row[10]
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        return([str(e)],''),['error']
    return result,field_names
    #return result[1][4].split("\n")

def inception_check(hosttag,sql,request):
    a = Db_name.objects.filter(dbtag=hosttag)[0]
    #a = Db_name.objects.get(dbtag=hosttag)
    tar_dbname = a.dbname
    if (not cmp(sql,wrong_msg)):
        results,col = func.mysql_query(wrong_msg,user,passwd,host,int(port),dbname)
        return results,col,tar_dbname
    try:
        if a.instance.all().filter(role='write')[0]:
            tar_host = a.instance.all().filter(role='write')[0].ip
            tar_port = a.instance.all().filter(role='write')[0].port
    except Exception,e:
        try:
            tar_host = a.instance.all().filter(role='all')[0].ip
            tar_port = a.instance.all().filter(role='all')[0].port
        except Exception,e:
            wrongmsg = "select \"" +str(e).replace('"',"\"")+"\""
            results,col = func.mysql_query(wrongmsg,user,passwd,host,int(port),dbname)
            return results,col,tar_dbname
    for i in a.db_account_set.all():
        if i.role!='read':
            tar_username = i.user
            tar_passwd = i.passwd
    #print tar_port+tar_passwd+tar_username+tar_host
    results,col = incep_exec(sql,tar_username,tar_passwd,tar_host,tar_port,tar_dbname)
    return results,col,tar_dbname
def main():
    x,y= incep_exec("use chang ;create table test (id int);",'dbmonitor','dbmonitor','10.1.70.222',3306,'lepus')
    print type(x)
    for i in x:
        print x
    print y
if __name__=='__main__':
    main()