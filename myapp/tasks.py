from celery import task
import datetime
from myapp.models import Db_name,Db_account,Db_instance,Oper_log,Task,Incep_error_log
from myapp.include import inception as incept


@task
def process_runtask(hosttag,sqltext,mytask):
    results,col,tar_dbname = incept.inception_check(hosttag,sqltext,1)
    status='executed'
    c_time = mytask.create_time
    mytask.update_time = datetime.datetime.now()
    mytask.save()
    for row in results:
        try:
            inclog = Incep_error_log(myid=row[0],stage=row[1],errlevel=row[2],stagestatus=row[3],errormessage=row[4],\
                         sqltext=row[5],affectrow=row[6],sequence=row[7],backup_db=row[8],execute_time=row[9],sqlsha=row[10],\
                         create_time=c_time,finish_time=mytask.update_time)
            inclog.save()
            #if some error occured in inception_check stage
        except Exception,e:
            inclog = Incep_error_log(myid=999,stage='',errlevel=999,stagestatus='',errormessage=row[0],\
                         sqltext=e,affectrow=999,sequence='',backup_db='',execute_time='',sqlsha='',\
                         create_time=c_time,finish_time=mytask.update_time)
            inclog.save()
        if (int(row[2])!=0):
            status='executed failed'
            #record error message of incept exec
    mytask.status = status
    mytask.save()


def task_run(idnum,request):
    while 1:
        try:
            task = Task.objects.get(id=idnum)
        except:
            continue
        break
    if task.status!='executed' and task.status!='running' and task.status!='NULL':
        hosttag = task.dbtag
        sql = task.sqltext
        mycreatetime = task.create_time
        incept.log_incep_op(sql,hosttag,request,mycreatetime)
        status='running'
        task.status = status
        task.update_time = datetime.datetime.now()
        task.save()
        process_runtask.delay(hosttag,sql,task)
        return ''
    elif task.status=='NULL':
        return 'PLEASE CHECK THE SQL FIRST'
    else:
        return 'Already executed or in running'