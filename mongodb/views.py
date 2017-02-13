#coding=UTF-8
from django.shortcuts import render,render_to_response
from myapp.form import AddForm
from myapp.include import function as func
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
import mongo
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.
@login_required(login_url='/accounts/login/')
def mongodb_query(request):
    dblist = mongo.get_mongodb_list(request.user.username)
    #dblist = ['ymmSmsLogYm','table2','table3','table4']
    if request.method == 'POST' :
        form = AddForm(request.POST)

            #instancetag = request.POST['instancetag']
        choosedb = request.POST['choosedb']
        tblist = mongo.get_mongo_collection(choosedb, request.user.username)
        try:
            if request.POST.has_key('gettblist'):

                return render(request, 'mongodb_query.html', locals())
            elif request.POST.has_key('query'):
                #return HttpResponse(tablename)
                choosed_tb = request.POST['choosed_tb']
                if form.is_valid():
                    a = form.cleaned_data['a']
                data_list = mongo.get_mongo_data(a, choosedb, choosed_tb, request.user.username)
                print data_list
                return render(request,'mongodb_query.html',locals())

                # return render(request,'mongodb_query.html',{'form': form,'data_list':data_mongo,'col':"record",'tablelist':table_list,'choosed_table':tablename})
        except Exception,e:
            print e
            return render(request, 'mongodb_query.html', locals())
            #else:
                #return render(request, 'mongo_query.html', {'form': form })
        else:
            print "not valid"
            return render(request, 'mongodb_query.html', locals())
    else:
        form = AddForm()
        return render(request, 'mongodb_query.html', locals())
