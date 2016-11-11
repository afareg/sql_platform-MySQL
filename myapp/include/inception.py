import MySQLdb,sys,string,time,datetime
from django.contrib.auth.models import User
from myapp.include import function as func
from multiprocessing import Process
from myapp.models import Db_name,Db_account,Db_instance,Oper_log,Task
reload(sys)
sys.setdefaultencoding('utf8')
import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.message import Message
from email.header import Header


#'executed','executed failed','check not passed','check passed','running'
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
incp_host = get_config('settings','incp_host')
incp_port = int(get_config('settings','incp_port'))
incp_user = get_config('settings','incp_user')
incp_passwd = get_config('settings','incp_passwd')

#0 for check and 1 for execute
def incep_exec(sqltext,myuser,mypasswd,myhost,myport,mydbname,flag=0):
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
    results,col = incep_exec(sql,tar_username,tar_passwd,tar_host,tar_port,tar_dbname,flag)
    return results,col,tar_dbname

def process_runtask(hosttag,sqltext,mytask):
    results,col,tar_dbname = inception_check(hosttag,sqltext,1)
    status='executed'
    for row in results:
        if (int(row[2])!=0):
            status='executed failed'
    mytask.status = status
    mytask.update_time = datetime.datetime.now()
    mytask.save()

def task_run(idnum,request):
    task = Task.objects.get(id=idnum)
    if task.status!='executed':
        hosttag = task.dbtag
        sql = task.sqltext
        log_incep_op(sql,hosttag,request)
        p = Process(target=process_runtask, args=(hosttag,sql,task))
        p.start()
        status='running'
        task.status = status
        task.update_time = datetime.datetime.now()
        task.save()

#        return [],[],''
#    else:
#        return [],[],''

def task_check(idnum,request):
    task = Task.objects.get(id=idnum)
    if task.status!='executed':
        hosttag = task.dbtag
        sql = task.sqltext
        results,col,dbname = inception_check(hosttag,sql)
        status='check passed'
        for row in results:
            if (int(row[2])!=0):
                status='check not passed'
        task.status = status
        task.update_time = datetime.datetime.now()
        task.save()
        return results,col,dbname
    else:
        return [],[],''



def get_task_list(dbtag,request):
    username=request.user.username
    if request.user.has_perm('myapp.can_admin_task'):
        if (dbtag=='all'):
            task_list = Task.objects.order_by("-create_time")[0:50]
        else:
            task_list = Task.objects.filter(dbtag=dbtag).order_by("-create_time")[0:50]
    else:
        if (dbtag=='all'):
            task_list = Task.objects.filter(user=username).order_by("-create_time")[0:50]
        else:
            task_list = Task.objects.filter(dbtag=dbtag).filter(user=username).order_by("-create_time")[0:50]
    return task_list

def delete_task(idnum):
    task = Task.objects.get(id=idnum)
    if task.status!='executed':
        task.delete()

#add task to tasktable
def record_task(request,sqltext,dbtag):
    username = request.user.username
    #lastlogin = user.last_login+datetime.timedelta(hours=8)
    #create_time = datetime.datetime.now()+datetime.timedelta(hours=8)
    create_time = datetime.datetime.now()
    update_time = datetime.datetime.now()
    status='NULL'
    mytask = Task (user=username,sqltext=sqltext,create_time=create_time,update_time=update_time,dbtag=dbtag,status=status)
    mytask.save()
    return 1


def log_incep_op(sqltext,dbtag,request):
    user = User.objects.get(username=request.user.username)
    lastlogin = user.last_login
    create_time = datetime.datetime.now()
    username = user.username
    sqltype='incept'
    ipaddr = func.get_client_ip(request)
    log = Oper_log (user=username,sqltext=sqltext,sqltype=sqltype,login_time=lastlogin,create_time=create_time,dbname='',dbtag=dbtag,ipaddr=ipaddr)
    log.save()
    return 1


def main():
    x,y,z= incep_exec("insert into t2 values(2);",'test','test','10.1.70.220',3306,'test')
    print type(x)
    for i in x:
        print x
    print y
if __name__=='__main__':
    main()