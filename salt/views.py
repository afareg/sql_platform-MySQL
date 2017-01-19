#coding=UTF-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
import saltapi
import json
# Create your views here.

def salt_exec(request):
  return render(request, 'exec.html', locals())


def execute(request):
    if request.method == 'POST':
        try:
            tgt = request.POST.get('tgt', "")
            fun = request.POST.get('fun', "cmd.run")
            arg = request.POST.get('arg', "")
            sapi = saltapi.SaltAPI()

            isgp = int(request.POST.get('isgroup', "0"))
            print isgp
            print type(isgp)
            jid_auto = sapi.asyncMasterToMinion(tgt=tgt, fun=fun, arg=arg,group=isgp)
            print jid_auto
        except Exception,e:
            print e
    # context = {'jid_auto': ''}
    # tgt = request.POST.get('tgt', "")
    # fun = request.POST.get('fun', "cmd.run")
    # arg = request.POST.get('arg', "")
    return render_to_response('auto_execute.html', locals())


def getjobinfo(request):
    context = {}
    jid_auto = request.GET['jid_auto']
    # print jid_auto
    if jid_auto:
        where = int(request.GET.get('where','12376894567235'))
        if where == 12376894567235:
            result = '/salt/api/getjobinfo?jid_auto=%s&where=%s' % (jid_auto,0)
            return HttpResponse(result)
        else:
            hosts_result, host_result = saltapi.salt_query("select id,success,replace(replace(`return`,'\\\\n','</br>'),'\\\\t','&nbsp') from salt.salt_returns where jid='%s' limit %s,10000;" % (jid_auto,where) )
            # cursor = connection.cursor()
            # host_result = cursor.execute()
            # hosts_result = cursor.fetchall()
            where = len(hosts_result) + where
            result = []
            for host_result in hosts_result:
                # print "host_result"
                # print host_result
                if host_result[2]:
                    result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br><pre>%s</pre><br>' % (host_result[0],host_result[1],host_result[2].strip('"')))
                else :
                    if host_result[1]:
                        result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br/><pre>执行成功，但该命令无返回结果</pre><br/>' % (host_result[0],host_result[1]))
                    else :
                        result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br/><pre>执行失败！</pre><br/>' % (host_result[0],host_result[1]))
            context = {
                  "where":where,
                  "result":result
                }
        return HttpResponse(json.dumps(context))


def hardware_info(request):
    sapi = saltapi.SaltAPI()
    up_host = sapi.runner_status('status')['up']
    jid = []
    disk_all = {}
    for hostname in up_host:
        info_all = sapi.remote_noarg_execution(hostname, 'grains.items')

        disk_use = sapi.remote_noarg_execution(hostname, 'disk.usage')

        for key in disk_use:
            if disk_use[key]['capacity'] is None:
                continue
            disk_info = {key: int(disk_use[key]['capacity'][:-1])}
            print disk_info
            disk_all.update(disk_info)
            print "disk all"
            print disk_all
            disk_dic = {'disk': disk_all}
            info_all.update(disk_dic)
        disk_all = {}
        jid += [info_all]
        print jid
    return render(request, 'hardware_info.html', {'jyp': jid})