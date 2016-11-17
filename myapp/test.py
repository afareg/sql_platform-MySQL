import MySQLdb, sys, string, time, datetime
from django.db import connection, connections
from myapp.models import Db_name, Db_account, Db_instance, Oper_log, Task, Incep_error_log
from django.contrib.auth.models import User
from multiprocessing import Process
reload(sys)
sys.setdefaultencoding('utf8')
import ConfigParser
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/tmp/logger1.log',
                    filemode='w')

def get_config(group,config_name):
    config = ConfigParser.ConfigParser()
    config.readfp(open('/root/PycharmProjects/mypro/myapp/etc/config.ini','r'))
    config_value=config.get(group,config_name).strip(' ').strip('\'').strip('\"')
    return config_value

def filters(data):
    return data.strip(' ').strip('\n').strip('\br')

host = get_config('settings','host')
port = get_config('settings','port')
user = get_config('settings','user')
passwd = get_config('settings','passwd')
dbname = get_config('settings','dbname')
select_limit = int(get_config('settings','select_limit'))
export_limit = int(get_config('settings','export_limit'))
wrong_msg = get_config('settings','wrong_msg')
incp_host = get_config('settings','incp_host')
incp_port = int(get_config('settings','incp_port'))
incp_user = get_config('settings','incp_user')
incp_passwd = get_config('settings','incp_passwd')
public_user = get_config('settings','public_user')


def task_sche_run():
    try:
        print "starting scheduler task"
        make_sure_mysql_usable()
        task = Task.objects.filter(status='appointed').filter(sche_time__lte=datetime.datetime.now())
        if len(task)>0:
            for mytask in task:
                print "mytask_id"
                print mytask.id
                hosttag = mytask.dbtag
                status = 'running'
                sql = mytask.sqltext
                mytask.status = status
                mytask.update_time = datetime.datetime.now()
                make_sure_mysql_usable()
                mytask.save()
                Process(target=process_runtask, args=(hosttag, sql, mytask)).start()
    except Exception,e:
        print e



def incep_exec(sqltext,myuser,mypasswd,myhost,myport,mydbname,flag=0):
    logging.info(sqltext)
    if (int(flag)==0):
        flagcheck='--enable-check'
    elif(int(flag)==1):
        flagcheck='--enable-execute'
    myuser=myuser.encode('utf8')
    mypasswd = mypasswd.encode('utf8')
    myhost=myhost.encode('utf8')
    myport=int(myport)
    mydbname=mydbname.encode('utf8')
    sql1="/*--user=%s;--password=%s;--host=%s;%s;--port=%d;*/\
            inception_magic_start;\
            use %s;"% (myuser,mypasswd,myhost,flagcheck,myport,mydbname)
    sql2='inception_magic_commit;'
    sql = sql1 + sqltext + sql2
    try:
        conn=MySQLdb.connect(host=incp_host,user=incp_user,passwd=incp_passwd,db='',port=incp_port,use_unicode=True, charset="utf8")
        cur=conn.cursor()
        ret=cur.execute(sql)
        result=cur.fetchall()
        #num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        logging.info("resulting in incept exec!!")
        logging.info(result)
        #print field_names
        #for row in result:
        #    print row[0], "|",row[1],"|",row[2],"|",row[3],"|",row[4],"|",row[5],"|",row[6],"|",row[7],"|",row[8],"|",row[9],"|",row[10]
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        return([str(e)],''),['error']
    return result,field_names
    #return result[1][4].split("\n")

#flag=0 for check and 1 for execute
def inception_check(hosttag,sql,flag=0):
    make_sure_mysql_usable()
    a = Db_name.objects.get(dbtag=hosttag)
    #a = Db_name.objects.get(dbtag=hosttag)
    logging.info(a)
    tar_dbname = a.dbname
    if (not cmp(sql,wrong_msg)):
        results,col = mysql_query(wrong_msg,user,passwd,host,int(port),dbname)
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
            results,col = mysql_query(wrongmsg,user,passwd,host,int(port),dbname)
            return results,col,tar_dbname
    tag=0
    for i in a.db_account_set.all():
        if i.role=='admin':
            tar_username = i.user
            tar_passwd = i.passwd
            break
    #print tar_port+tar_passwd+tar_username+tar_host
    try:
        results,col = incep_exec(sql,tar_username,tar_passwd,tar_host,tar_port,tar_dbname,flag)
        return results,col,tar_dbname
    except Exception,e:
        wrongmsg = "select \"no admin account being setted\""
        results, col = mysql_query(wrongmsg, user, passwd, host, int(port), dbname)
        return results, col, tar_dbname


def process_runtask(hosttag,sqltext,mytask):
    time.sleep(1)
    results,col,tar_dbname = inception_check(hosttag,sqltext,1)
    status='executed'
    c_time = mytask.create_time
    mytask.update_time = datetime.datetime.now()
    make_sure_mysql_usable()
    mytask.save()
    for row in results:
        try:
            inclog = Incep_error_log(myid=row[0],stage=row[1],errlevel=row[2],stagestatus=row[3],errormessage=row[4],\
                         sqltext=row[5],affectrow=row[6],sequence=row[7],backup_db=row[8],execute_time=row[9],sqlsha=row[10],\
                         create_time=c_time,finish_time=mytask.update_time)
            make_sure_mysql_usable()
            inclog.save()
        except Exception,e:
            inclog = Incep_error_log(myid=999,stage='',errlevel=999,stagestatus='',errormessage=row[0],\
                         sqltext=e,affectrow=999,sequence='',backup_db='',execute_time='',sqlsha='',\
                         create_time=c_time,finish_time=mytask.update_time)
            make_sure_mysql_usable()
            inclog.save()
        if (int(row[2])!=0):
            status='executed failed'
            #record error message of incept exec
    mytask.status = status
    make_sure_mysql_usable()
    mytask.save()

def make_sure_mysql_usable():
    # mysql is lazily connected to in django.
    # connection.connection is None means
    # you have not connected to mysql before
    if connection.connection and not connection.is_usable():
        # destroy the default mysql connection
        # after this line, when you use ORM methods
        # django will reconnect to the default mysql
        del connections._connections.default


def mysql_query(sql,user=user,passwd=passwd,host=host,port=int(port),dbname=dbname,limitnum=select_limit):
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
        #result=cursor.fetchall()
        result=cursor.fetchmany(size=int(limitnum))
        cursor.close()
        conn.close()
        return (result,col)
    except Exception,e:
        return([str(e)],''),['error']