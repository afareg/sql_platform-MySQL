from django.contrib.auth.models import User,Permission,ContentType,Group
from myapp.models import Db_name,Db_group,Db_account,Db_instance,Oper_log,Login_log

#function for db_group.html
def get_full():
    dbgrouplist =  Db_group.objects.all()
    userlist = User.objects.all()
    dbnamelist = Db_name.objects.all()
    return dbgrouplist,userlist,dbnamelist

def get_group_detail(groupname):
    group = Db_group.objects.get(groupname=groupname)
    a = group.dbname.all()
    b = group.account.all()
    return a,b

def set_dbgroup(groupname,dbnamesetlist,usersetlist):
    gp = Db_group.objects.get(groupname=groupname)
    new_db = Db_name.objects.filter(dbtag__in=dbnamesetlist)
    old_db = gp.dbname.all()
    new_user = User.objects.filter(username__in=usersetlist)
    old_user = gp.account.all()
    new_dbli = []
    old_dbli = []
    new_userli = []
    old_userli = []
    for i in new_db:
        new_dbli.append(i.dbtag)
    for i in old_db:
        old_dbli.append(i.dbtag)
    for i in new_user:
        new_userli.append(i.username)
    for i in old_user:
        old_userli.append(i.username)

    add_user = list(set(new_userli).difference(set(old_userli)))
    del_user = list(set(old_userli).difference(set(new_userli)))
    inter_user = list(set(old_userli).intersection(set(new_userli)))
    add_db = list(set(new_dbli).difference(set(old_dbli)))
    del_db = list(set(old_dbli).difference(set(new_dbli)))

    #del user handle
    for i in User.objects.filter(username__in=del_user):
        try:
            existdbli = get_exist_db(groupname, i, old_dbli)
            gp.account.remove(i)
            for x in old_db:
                try:
                    #if dbtag already owned by user in other group ,then don't remove
                    if x.dbtag not in existdbli:
                        x.account.remove(i)
                except Exception,e:
                    pass
        except Exception, e:
            pass

    #add user handle
    for i in User.objects.filter(username__in=add_user):
        try:
            gp.account.add(i)
            for x in new_db:
                try:
                    x.account.add(i)
                except Exception,e:
                    pass
        except Exception, e:
            pass

    #exists user handle
    for i in User.objects.filter(username__in=inter_user):
        existdbli = get_exist_db(groupname, i, old_dbli)
        for x in Db_name.objects.filter(dbtag__in=add_db) :
            if x.dbtag in existdbli:
                pass
            else:
                try:
                    x.account.add(i)
                except Exception,e:
                    pass

        for x in Db_name.objects.filter(dbtag__in=del_db) :
            if x.dbtag in existdbli:
                pass
            else:
                try:
                    x.account.remove(i)
                except Exception,e:
                    pass

    for i in Db_name.objects.filter(dbtag__in=add_db):
        try:
            gp.dbname.add(i)
        except Exception,e:
            pass

    for i in Db_name.objects.filter(dbtag__in=del_db):
        try:
            gp.dbname.remove(i)
        except Exception,e:
            pass

    return new_db,new_user


def del_dbgroup(groupname):
    gp = Db_group.objects.get(groupname=groupname)
    old_db = gp.dbname.all()
    old_user = gp.account.all()
    old_dbli = []
    for i in old_db:
        old_dbli.append(i.dbtag)
    for i in old_user:
        existdbli = get_exist_db(groupname, i, old_dbli)
        for x in old_db:
            if x.dbtag in existdbli:
                pass
            else:
                try:
                    x.account.remove(i)
                except Exception, e:
                    pass
    gp.delete()


def get_exist_db (groupname,user,old_dbli):
    # gp = Db_group.objects.get(groupname=groupname)
    exist_db = []
    for i in user.db_group_set.exclude(groupname=groupname):
        for x in i.dbname.filter(dbtag__in=old_dbli):
            exist_db.append(x.dbtag)

    return list(set(exist_db))



def create_dbgroup(groupname,dbnamesetlist,usersetlist):
    mydbname = Db_name.objects.filter(dbtag__in=dbnamesetlist)
    myuser = User.objects.filter(username__in=usersetlist)
    new_group = Db_group(groupname=groupname)
    new_group.save()
    for i in mydbname:
        try:
            new_group.dbname.add(i)
        except Exception,e:
            pass
        for x in myuser:
            try:
                i.account.add(x)
            except Exception,e:
                pass
    for i in myuser:
        try:
            new_group.account.add(i)
        except Exception,e:
            pass
    return mydbname,myuser



#u_group.html
def get_full_per():
    a = Group.objects.all()
    b = Permission.objects.filter(codename__istartswith='can')
    c = User.objects.all()
    return a,b,c

def get_ugroup_detail(groupname):
    group = Group.objects.get(name=groupname)
    a = group.permissions.all()
    b = group.user_set.all()
    return a,b

def create_ugroup(groupname,persetlist,usersetlist):
    group = Group(name=groupname)
    group.save()
    perli = Permission.objects.filter(codename__in=persetlist)
    userli = User.objects.filter(username__in=usersetlist)
    for i in perli:
        try:
            group.permissions.add(i)
        except Exception,e:
            pass
    for i in userli :
        try:
            group.user_set.add(i)
        except Exception,e:
            pass
    return perli,userli

def del_ugroup(groupname):
    group = Group.objects.get(name=groupname)
    group.delete()


