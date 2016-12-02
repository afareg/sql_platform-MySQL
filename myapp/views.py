import sys,json,os,datetime,csv
from django.contrib import admin
from django.template.context import RequestContext
from ratelimit.decorators import ratelimit,is_ratelimited
from django.shortcuts import render,render_to_response
from django.contrib import auth
from form import AddForm,LoginForm,Logquery,Uploadform,Captcha,Taskquery,Taskscheduler,Dbgroupform
from captcha.fields import CaptchaField,CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import User,Permission,ContentType,Group
from myapp.include import function as func,inception as incept,chart,pri
from myapp.models import Db_group,Db_name,Db_account,Db_instance,Oper_log,Upload,Task
from django.core.files import File
#path='./myapp/include'
#sys.path.insert(0,path)
#import function as func
# Create your views here.
'''
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
'''

@login_required(login_url='/accounts/login/')
def index(request):
    data,col = chart.get_main_chart()
    taskdata,taskcol = chart.get_task_chart()
    bingtu = chart.get_task_bingtu()
    # print json.dumps(bingtu)
    return render(request, 'include/base.html',{'bingtu':json.dumps(bingtu),'data':json.dumps(data),'col':json.dumps(col),'taskdata':json.dumps(taskdata),'taskcol':json.dumps(taskcol)})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")

@login_required(login_url='/accounts/login/')
@permission_required('myapp.can_log_query', login_url='/')
def log_query(request):
    #show every dbtags
    #obj_list = func.get_mysql_hostlist(request.user.username,'log')
    #show dbtags permitted to the user
    obj_list = func.get_mysql_hostlist(request.user.username)
    optype_list = func.get_op_type()
    if request.method == 'POST' :
        form = Logquery(request.POST)
        if form.is_valid():
            begintime = form.cleaned_data['begin']
            endtime = form.cleaned_data['end']
            hosttag = request.POST['hosttag']
            optype = request.POST['optype']
            data = func.get_log_data(hosttag,optype,begintime,endtime)
            return render(request,'log_query.html',{'form': form,'objlist':obj_list,'optypelist':optype_list,'datalist':data,'choosed_host':hosttag})
        else:
            print "not valid"
            return render(request,'log_query.html',{'form': form,'objlist':obj_list,'optypelist':optype_list})
    else:
        form = Logquery()
        return render(request, 'log_query.html', {'form': form,'objlist':obj_list,'optypelist':optype_list})


@login_required(login_url='/accounts/login/')
@permission_required('myapp.can_mysql_query', login_url='/')
def mysql_query(request):
    #print request.user.username
    # print request.user.has_perm('myapp.can_mysql_query')
    obj_list = func.get_mysql_hostlist(request.user.username)
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            c = request.POST['cx']
            try:
                #show explain
                if request.POST.has_key('explain'):
                    a = func.check_explain (a)
                    (data_mysql,collist,dbname) = func.get_mysql_data(c,a,request.user.username,request,100)
                    return render(request,'mysql_query.html',{'form': form,'objlist':obj_list,'data_list':data_mysql,'col':collist,'choosed_host':c,'dbname':dbname})
                    #export csv
                elif request.POST.has_key('export'):
                    a,numlimit = func.check_mysql_query(a,request.user.username,'export')
                    (data_mysql,collist,dbname) = func.get_mysql_data(c,a,request.user.username,request,numlimit)
                    pseudo_buffer = Echo()
                    writer = csv.writer(pseudo_buffer)
                    #csvdata =  (collist,'')+data_mysql
                    i=0
                    results_long = len(data_mysql)
                    results_list = [None] * results_long
                    for i in range(results_long):
                        results_list[i] = list(data_mysql[i])
                    results_list.insert(0,collist)
                    a = u'zhongwen'
                    for result in results_list:
                        i=0
                        for item in result:
                            if type(item) == type(a):
                                result[i] = item.encode('gb2312')
                            i = i + 1
                    response = StreamingHttpResponse((writer.writerow(row) for row in results_list),content_type="text/csv")
                    response['Content-Disposition'] = 'attachment; filename="export.csv"'
                    return response
                elif request.POST.has_key('query'):
                #get nomal query
                    a,numlimit = func.check_mysql_query(a,request.user.username)
                    # print type(a)
                    # print a
                    (data_mysql,collist,dbname) = func.get_mysql_data(c,a,request.user.username,request,numlimit)
                    return render(request,'mysql_query.html',{'form': form,'objlist':obj_list,'data_list':data_mysql,'col':collist,'choosed_host':c,'dbname':dbname})
            except Exception,e:
                print e
                return render(request, 'mysql_query.html', {'form': form, 'objlist': obj_list})
        else:
            return render(request, 'mysql_query.html', {'form': form,'objlist':obj_list})
    else:
        form = AddForm()
        return render(request, 'mysql_query.html', {'form': form,'objlist':obj_list})

class Echo(object):
    """An object that implements just the write method of the file-like interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value
'''
def some_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    data = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in data),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="test.csv"'
    return response
'''



@login_required(login_url='/accounts/login/')
@permission_required('myapp.can_see_execview', login_url='/')
def mysql_exec(request):
    #print request.user.username
    obj_list = func.get_mysql_hostlist(request.user.username,'exec')
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            c = request.POST['cx']
            a = func.check_mysql_exec(a,request)
            #print request.POST
            if request.POST.has_key('commit'):
                (data_mysql,collist,dbname) = func.run_mysql_exec(c,a,request.user.username,request)
            elif request.POST.has_key('check'):
                data_mysql,collist,dbname = incept.inception_check(c,a)
            return render(request,'mysql_exec.html',{'form': form,'objlist':obj_list,'data_list':data_mysql,'col':collist,'choosed_host':c,'dbname':dbname})

        else:
            return render(request, 'mysql_exec.html', {'form': form,'objlist':obj_list})
    else:
        form = AddForm()
        return render(request, 'mysql_exec.html', {'form': form,'objlist':obj_list})

        '''
            upform = Uploadform(request.POST,request.FILES)
            c = request.POST['cx']
            form = AddForm()
            sqltext=''
            for chunk in request.FILES['filename'].chunks():
                sqltext = sqltext + chunk
            print sqltext
        '''
@login_required(login_url='/accounts/login/')
def inception(request):
    obj_list = func.get_mysql_hostlist(request.user.username,'incept')
    if request.method == 'POST':
        specification = request.POST['specification'][0:30]
        if request.POST.has_key('check'):
            form = AddForm(request.POST)
            upform = Uploadform()
            if form.is_valid():
                a = form.cleaned_data['a']
                c = request.POST['cx']
                data_mysql,collist,dbname = incept.inception_check(c,a)
                return render(request, 'inception.html', {'form': form,'upform':upform,'objlist':obj_list,'data_list':data_mysql,'col':collist,'choosed_host':c})
            else:
                print "not valid"
                return render(request, 'inception.html', {'form': form,'upform':upform,'objlist':obj_list})
        elif request.POST.has_key('upload'):
            upform = Uploadform(request.POST,request.FILES)
            #c = request.POST['cx']
            if upform.is_valid():
                c = request.POST['cx']
                sqltext=''
                for chunk in request.FILES['filename'].chunks():
                    #print chunk
                    try:
                        chunk = chunk.decode('utf8')
                    except Exception,e:
                        chunk = chunk.decode('gbk')
                    sqltext = sqltext + chunk
                form = AddForm(initial={'a': sqltext})
                return render(request, 'inception.html', {'form': form,'upform':upform,'objlist':obj_list,'choosed_host':c})
            else:
                form = AddForm()
                upform = Uploadform()
                return render(request, 'inception.html', {'form': form,'upform':upform,'objlist':obj_list})
        elif request.POST.has_key('addtask'):
            form = AddForm(request.POST)
            upform = Uploadform()
            if form.is_valid():
                sqltext = form.cleaned_data['a']
                c = request.POST['cx']
                incept.record_task(request,sqltext,c,specification)
                status='UPLOAD TASK OK'
                return render(request, 'inception.html', {'form': form,'upform':upform,'objlist':obj_list,'status':status})
            else:
                status='UPLOAD TASK FAIL'
                return render(request, 'inception.html', {'form': form,'upform':upform,'objlist':obj_list,'status':status})
    else:
        form = AddForm()
        upform = Uploadform()
        return render(request, 'inception.html', {'form': form,'upform':upform,'objlist':obj_list})


#@ratelimit(key=func.my_key,method='POST', rate='5/15m')
def login(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        form = LoginForm()
        myform = Captcha()
        error = 1
        return render_to_response('login.html', RequestContext(request, {'form': form,'myform':myform,'error':error}))
    else:
        if request.user.is_authenticated():
            return render(request, 'include/base.html')
        else:
            if request.GET.get('newsn')=='1':
                csn=CaptchaStore.generate_key()
                cimageurl= captcha_image_url(csn)
                return HttpResponse(cimageurl)
            elif  request.method == "POST":
                form = LoginForm(request.POST)
                myform = Captcha(request.POST)
                if myform.is_valid():
                    if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
                        user = auth.authenticate(username=username, password=password)
                        if user is not None and user.is_active:
                            auth.login(request, user)
                            func.log_userlogin(request)
                            return HttpResponseRedirect("/")
                        else:
                            #login failed
                            func.log_loginfailed(request, username)
                            #request.session["wrong_login"] =  request.session["wrong_login"]+1
                            return render_to_response('login.html', RequestContext(request, {'form': form,'myform':myform,'password_is_wrong':True}))
                    else:
                        return render_to_response('login.html', RequestContext(request, {'form': form,'myform':myform}))
                else :
                    #cha_error
                    form = LoginForm(request.POST)
                    myform = Captcha(request.POST)
                    chaerror = 1
                    return render_to_response('login.html', RequestContext(request, {'form': form,'myform':myform,'chaerror':chaerror}))
            else:
                form = LoginForm()
                myform = Captcha()
                return render_to_response('login.html', RequestContext(request, {'form': form,'myform':myform}))





#
# @login_required(login_url='/accounts/login/')
# def upload_file(request):
#     if request.method == "POST":
#         form = Uploadform(request.POST,request.FILES)
#         if form.is_valid():
#         #username = request.user.username
#             username ='test'
#             filename = form.cleaned_data['filename']
#             myfile = Upload()
#             myfile.username = username
#             myfile.filename = filename
#             myfile.save()
#             print myfile.filename.url
#             print myfile.filename.path
#             print myfile.filename.name
#             print ""
#             for chunk in request.FILES['filename'].chunks():
#                 sqltext = sqltext + chunk
#             print sqltext
#             f = open(myfile.filename.path,'r')
#             result = list()
#             for line in f.readlines():
#                 #print line
#                 result.append(line)
#             print "what the fuck"
#             print result
#             return HttpResponse('upload ok!')
#         else :
#             return HttpResponse('upload false!')
#     else:
#         form = Uploadform()
#         return  render(request, 'upload.html', {'form': form})

@login_required(login_url='/accounts/login/')
def task_manager(request):
    #obj_list = func.get_mysql_hostlist(request.user.username,'log')
    obj_list = ['all'] + func.get_mysql_hostlist(request.user.username,'incept')
    if request.method == 'POST' :
        form = Taskquery(request.POST)
        form2 = Taskscheduler(request.POST)
        if form.is_valid():
            endtime = form.cleaned_data['end']
        else:
            endtime = datetime.datetime.now()
        if form2.is_valid():
            sche_time = form2.cleaned_data['sche_time']
            # print sche_time
        else:
            sche_time = datetime.datetime.now()
        hosttag = request.POST['hosttag']
        data = incept.get_task_list(hosttag, request, endtime)
        if request.POST.has_key('commit'):
            data = incept.get_task_list(hosttag,request,endtime)
            return render(request,'task_manager.html',{'form':form,'form2':form2,'objlist':obj_list,'datalist':data,'choosed_host':hosttag})
        elif request.POST.has_key('delete'):
            id = int(request.POST['delete'])
            incept.delete_task(id)
            return render(request,'task_manager.html',{'form':form,'form2':form2,'objlist':obj_list,'datalist':data,'choosed_host':hosttag})
        elif request.POST.has_key('check'):
            id = int(request.POST['check'])
            results,col,tar_dbname = incept.task_check(id,request)
            return render(request,'task_manager.html',{'form':form,'form2':form2,'objlist':obj_list,'datalist':data,'choosed_host':hosttag,'result':results,'col':col})
        elif request.POST.has_key('see_running'):
            id = int(request.POST['see_running'])
            results,cols = incept.task_running_status(id)
            return render(request,'task_manager.html',{'form':form,'form2':form2,'objlist':obj_list,'datalist':data,'choosed_host':hosttag,'result_status':results,'cols':cols})
        elif request.POST.has_key('exec'):
            id = int(request.POST['exec'])
            nllflag = incept.task_run(id,request)
            # print nllflag
            return render(request,'task_manager.html',{'form':form,'form2':form2,'objlist':obj_list,'datalist':data,'choosed_host':hosttag,'nllflag':nllflag})
        elif request.POST.has_key('stop'):
            sqlsha = request.POST['stop']
            incept.incep_stop(sqlsha)
            results,cols  = incept.incep_stop(sqlsha)
            return render(request,'task_manager.html',{'form':form,'form2':form2,'objlist':obj_list,'datalist':data,'choosed_host':hosttag,'result_status':results,'cols':cols})
        elif request.POST.has_key('appoint'):
            id = int(request.POST['appoint'])
            incept.set_schetime(id,sche_time)
            return render(request, 'task_manager.html',{'form': form,'form2':form2, 'objlist': obj_list, 'datalist': data, 'choosed_host': hosttag})
        elif request.POST.has_key('update'):
            id = int(request.POST['update'])
            request.session['update_taskid']=id
            return HttpResponseRedirect("/update_task/")
    else:
        data = incept.get_task_list('all',request,datetime.datetime.now())
        form = Taskquery()
        form2 = Taskscheduler()
        return render(request, 'task_manager.html', {'form':form,'form2':form2,'objlist':obj_list,'datalist':data})



@login_required(login_url='/accounts/login/')
def update_task(request):
    try:
        id = request.session['update_taskid']
    except Exception,e:
        str = "ERROR"
        return render(request, 'update_task.html', {'str': str})
    if request.method == 'POST':
        flag,str = incept.check_task_status(id)
        if flag:
            sqltext = request.POST['sqltext']
            specify = request.POST['specify'][0:30]
            incept.update_task(id, sqltext, specify)
            return HttpResponseRedirect("/task/")
        else:
            return render(request, 'update_task.html', {'str': str})
    else:
        try:
            data = incept.get_task_forupdate(id)
            return render(request, 'update_task.html', {'data': data})
        except Exception,e:
            str = "ID NOT EXISTS , PLEASE CHECK !"
            return render(request, 'update_task.html', {'str': str})


@login_required(login_url='/accounts/login/')
@permission_required('myapp.can_query_pri', login_url='/')
def pre_query(request):
    objlist = func.get_mysql_hostlist(request.user.username,'log')
    usergroup = Db_group.objects.all()
    if request.method == 'POST':
        if request.POST.has_key('queryuser'):
        # if request.POST.has_key('accountname') and request.POST['accountname']!='':
            try:
                username = request.POST['accountname']
                dbgp, usergp = func.get_user_grouppri(username)

                pri = func.get_privileges(username)
                profile = []
                try:
                    profile = User.objects.get(username=username).user_profile
                except Exception,e:
                    pass
                userdblist,info = func.get_user_pre(username,request)
                return render(request, 'previliges/prequery.html', {'pri':pri, 'profile':profile, 'dbgp':dbgp, 'usergp':usergp, 'objlist':objlist, 'userdblist': userdblist, 'info':info, 'usergroup':usergroup})
            except Exception,e:
                return render(request, 'previliges/prequery.html', {'objlist':objlist, 'usergroup':usergroup})
        elif request.POST.has_key('querydb'):
            try:
                choosed_host = request.POST['cx']
                data,instance,acc = func.get_pre(choosed_host)
                return render(request, 'previliges/prequery.html', {'objlist':objlist, 'choosed_host':choosed_host, 'data_list':data, 'ins_list':instance, 'acc':acc, 'usergroup':usergroup})
            except Exception, e:
                return render(request, 'previliges/prequery.html', {'objlist': objlist, 'usergroup': usergroup})
        elif request.POST.has_key('querygp'):
            try:
                choosed_gp = request.POST['choosed_gp']
                dbgroup = func.get_groupdb(choosed_gp)
                return render(request, 'previliges/prequery.html', {'objlist': objlist, 'dbgroup':dbgroup, 'usergroup': usergroup})
            except Exception,e:
                return render(request, 'previliges/prequery.html', {'objlist': objlist, 'usergroup': usergroup})
    else:
        return render(request, 'previliges/prequery.html', {'objlist':objlist, 'usergroup':usergroup})



@login_required(login_url='/accounts/login/')
@permission_required('myapp.can_set_pri', login_url='/')
def pre_set(request):
    userlist,grouplist = func.get_UserAndGroup()
    usergroup=func.get_usergp_list()
    dblist = Db_name.objects.all()
    if request.method == 'POST':
        username = request.POST['account']
        if request.POST.has_key('set'):
            try :
                dbgplist = request.POST.getlist('choosedlist')
                group = request.POST.getlist('user_group')
                ch_db = request.POST.getlist('user_dblist')
                func.clear_userpri(username)
                func.set_groupdb(username,dbgplist)
                user = User.objects.get(username=username)
                func.set_usergroup(user, group)
                func.set_user_db(user, ch_db)
                info = 'SET USER ' + username + '  OK!'
                return render(request, 'previliges/pre_set.html', {'info':info, 'dblist':dblist, 'userlist': userlist, 'grouplist': grouplist, 'usergroup':usergroup})
            except Exception,e:
                info = 'SET USER ' + username + '  FAILED!'
                return render(request, 'previliges/pre_set.html', {'info':info, 'dblist':dblist, 'userlist': userlist, 'grouplist': grouplist, 'usergroup':usergroup})
        elif request.POST.has_key('reset'):
            func.clear_userpri(username)
            info = 'RESET USER '+ username + '  OK!'
            return render(request, 'previliges/pre_set.html', {'info':info, 'dblist':dblist, 'userlist': userlist, 'grouplist': grouplist, 'usergroup':usergroup})
        elif request.POST.has_key('query'):
            dbgp,usergp = func.get_user_grouppri(username)
            userdblist,info = func.get_user_pre(username, request)
            return render(request, 'previliges/pre_set.html', {'username':username, 'dbgp':dbgp, 'usergp':usergp, 'userdblist':userdblist, 'dblist':dblist, 'userlist': userlist, 'grouplist': grouplist, 'usergroup':usergroup})
        elif request.POST.has_key('delete'):
            try:
                info = 'DELETE USER ' + username + '  OK!'
                func.delete_user(username)
                return render(request, 'previliges/pre_set.html',{'info': info, 'dblist': dblist, 'userlist': userlist, 'grouplist': grouplist,'usergroup': usergroup})
            except Exception,e:
                info = 'DELETE USER ' + username + '  FAILED!'
                return render(request, 'previliges/pre_set.html', {'info': info, 'dblist': dblist, 'userlist': userlist, 'grouplist': grouplist,'usergroup': usergroup})
        elif  request.POST.has_key('create'):
            try:
                username = request.POST['newname']
                passwd = request.POST['newpasswd']
                group = request.POST.getlist('user_group')
                dbgplist = request.POST.getlist('choosedlist')
                ch_db = request.POST.getlist('user_dblist')
                user = func.create_user(username,passwd)
                func.set_groupdb(username, dbgplist)
                func.set_user_db(user, ch_db)
                func.set_usergroup(user,group)
                info = "CREATE USER SUCCESS!"
                return render(request, 'previliges/pre_set.html', {'info':info, 'dblist':dblist, 'userlist': userlist, 'grouplist': grouplist, 'usergroup':usergroup})
            except Exception,e:
                info = "CREATE USER FAILED!"
                return render(request, 'previliges/pre_set.html', {'info':info, 'dblist':dblist, 'userlist': userlist, 'grouplist': grouplist, 'usergroup':usergroup})
    else:
        return render(request, 'previliges/pre_set.html', {'dblist':dblist, 'userlist':userlist, 'grouplist':grouplist, 'usergroup':usergroup})


def set_dbgroup(request):
    dbgrouplist,userlist,dbnamelist = pri.get_full()
    if request.method == 'POST':
        if request.POST.has_key('query'):
            try:
                groupname = request.POST['dbgroup_set']
                s_dbnamelist,s_userlist = pri.get_group_detail(groupname)
                return render(request, 'previliges/db_group.html', locals())
            except Exception,e:
                return render(request, 'previliges/db_group.html', locals())
        elif request.POST.has_key('create'):
            try:
                info = "CREATE OK!"
                groupname = request.POST['newname']
                dbnamesetlist = request.POST.getlist('dbname_set')
                usersetlist = request.POST.getlist('user_set')
                s_dbnamelist,s_userlist = pri.create_dbgroup(groupname,dbnamesetlist,usersetlist)
                return render(request, 'previliges/db_group.html', locals())
            except Exception,e:
                info = "CREATE FAILED!"
                return render(request, 'previliges/db_group.html', locals())
        elif request.POST.has_key('set'):
            try:
                info = "SET OK!"
                groupname = request.POST['dbgroup_set']
                a =request.POST.getlist('dbname_set')
                b =  request.POST.getlist('user_set')
                s_dbnamelist, s_userlist = pri.set_dbgroup(groupname, a, b)
                return render(request, 'previliges/db_group.html', locals())
            except Exception,e:
                info = "SET FAILED"
                return render(request, 'previliges/db_group.html', locals())

        elif request.POST.has_key('delete'):
            try:
                info = "DELETE OK!"
                groupname = request.POST['dbgroup_set']
                pri.del_dbgroup(groupname)
                return render(request, 'previliges/db_group.html', locals())
            except Exception,e:
                info = "DELETE FAILED!"
                return render(request, 'previliges/db_group.html', locals())
    else:
        return render(request,'previliges/db_group.html',locals())


def set_ugroup(request):
    grouplist, perlist,userlist = pri.get_full_per()
    if request.method == 'POST':
        if request.POST.has_key('query'):
            try:
                groupname = request.POST['group_set']
                s_perlist,s_userlist = pri.get_ugroup_detail(groupname)
                return render(request, 'previliges/u_group.html', locals())
            except Exception,e:
                return render(request, 'previliges/u_group.html', locals())
        elif request.POST.has_key('create'):
            try:
                info = "CREATE OK!"
                groupname = request.POST['newname']
                persetlist = request.POST.getlist('per_set')
                usersetlist = request.POST.getlist('user_set')
                s_perlist,s_userlist = pri.create_ugroup(groupname,persetlist,usersetlist)
                return render(request, 'previliges/u_group.html', locals())
            except Exception,e:
                info = "CREATE FAILED!"
                return render(request, 'previliges/u_group.html', locals())
        elif request.POST.has_key('delete'):
            try:
                groupname = request.POST['group_set']
                info = "DELETE OK!"
                pri.del_ugroup(groupname)
                return render(request, 'previliges/u_group.html', locals())
            except Exception,e:
                info = "DELETE FAILED!"
                return render(request, 'previliges/u_group.html', locals())
        elif request.POST.has_key('set'):
            try:
                info = "SET OK!"
                groupname = request.POST['group_set']
                persetlist = request.POST.getlist('per_set')
                usersetlist = request.POST.getlist('user_set')
                pri.del_ugroup(groupname)
                s_perlist, s_userlist = pri.create_ugroup(groupname, persetlist,usersetlist)
                return render(request, 'previliges/u_group.html', locals())
            except Exception,e:
                info = "SET FAILED!"
                return render(request, 'previliges/u_group.html', locals())
    else:
        return render(request, 'previliges/u_group.html', locals())


@ratelimit(key=func.my_key, rate='5/h')
def test(request):
    was_limited = getattr(request, 'limited', False)
    print  was_limited
    return render(request, 'test.html')
