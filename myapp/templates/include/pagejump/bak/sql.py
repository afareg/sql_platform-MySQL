exceptlist = ["'","`","\""]
def sqlparse(sqlfull):
    tmp = oldp = sql = ''
    sqllist = []
    flag = 0
    sqlfull = sqlfull.replace('\r','\n').strip()

    try:
        if sqlfull[-1]!=";":
            sqlfull = sqlfull + ";"
    except Exception,e:
        pass
    for i in sqlfull.split('\n'):
        if len(i)>=2:
            if i[0] == '-' and i[1] == '-' :
                continue
        if len(i)>=1:
            if i[0] == '#' :
                continue
        tmp = tmp + i+'\n'
    sqlfull = tmp
    tmp = ''
    i=0
    while i<= (0 if len(sqlfull)==0 else len(sqlfull)-1):
        if sqlfull[i] =='*' and oldp == '/'and flag == 0 :
            flag = 2
            sql = sql + sqlfull[i]
        elif sqlfull[i] == '/' and oldp == '*' and flag == 2:
            flag = 0
            sql = sql + sqlfull[i]
        elif sqlfull[i] == tmp and flag == 1:
            flag = 0
            sql = sql + sqlfull[i]
            tmp=''
        elif sqlfull[i] in exceptlist and flag == 0 and oldp != "\\":
            tmp = sqlfull[i]
            flag = 1
            sql = sql + sqlfull[i]
        elif sqlfull[i] == ';' and flag == 0:
            sql = sql + sqlfull[i]
            if len(sql) > 1:
                sqllist.append(sql)
            sql = ''
        elif sqlfull[i] == '#' and flag == 0:
            flag =3
        elif flag==3:
            if sqlfull[i] == '\n':
                flag=0
                sql = sql + sqlfull[i]
        else:
            sql = sql + sqlfull[i]
        oldp = sqlfull[i]
        i=i+1
    return sqllist


def get_sqltype(sqllist):
    query_type = ['desc','describe','show','select','explain']
    dml_type = ['insert', 'update', 'delete', 'create', 'alter', 'drop', 'truncate', 'replace']
    list_type = query_type
    typelist = []
    i = 0
    while i <= (0 if len(sqllist) == 0 else len(sqllist) - 1):
        try:
            type = sqllist[i].split()[0].lower()
            if len(type)> 1:
                if type in list_type:
                    typelist.append(type)
                    i = i + 1
                else:
                    sqllist.pop(i)
            else:
                sqllist.pop(i)
        except:
            pass
            i = i + 1

    return sqllist

if __name__ == '__main__':
    x = "  #adfadfaf \nselect adf;  create /*\\'\" test */ table test (id int ,name varchar(30)) comment 'asdasdasd';\n;/*! test &&\''& */\r\n;\r\n/*!40101 SET character_set_client = @saved_cs_client */;;\r\n;;;select /* force index test \'\"*/ * from test ;"
    #x="select \"  \'\"\'\";"
    # print x
    x=" /*! */; select /**/ #asdfasdf; \nfrom mysql_replication_history;"
    sqllist = sqlparse(x)
    for i in sqllist:
        print i
    print  get_sqltype(sqllist)
