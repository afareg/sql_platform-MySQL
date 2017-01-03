# sql_manage_platform-MySQL
## 基于django和inception，带权限控制的mysql语句运行平台
### 另外还带有一些简单的监控功能
### 开发环境：
#### django:1.8.14
#### python:2.7.12
#### MySQL和redis实例各一个
### python依赖组件：
#### django-celery 3.1.17
#### celery 3.1.25
#### kombu 3.0.37
#### celery-with-redis 3.0
#### django-simple-captcha
#### MySQL-python
### 权限功能简述：
用户的系统使用权限大致可以分为可以看到的页面，以及能够看到的DB两个维度

这两个维度的权限都可以通过设置组来达到后期快速添加用户的需求

对于前者：

所有页面都可以根据需要分配给不同权限的用户

对于DB维度的权限：

一个DB可以配置role为read和write两个ip-port实例，用以区分查询和变更语句执行的实例，（也可以将role配置成all不进行区分）

对于数据库账户，一个DB可以配置多个，并分配给不同的用户，用以实现不同用户在同一db下区分权限的功能。（也可以保持默认设置，即分配给public用户，不进行区分）

如果要使用任务管理功能，需要为DB添加一个role为admin的数据库账号
。。。待续

### 启动配置
#### config.py配置文件如下：

wrong_msg="select '请检查输入语句'"

select_limit=200

export_limit=200

incp_host="x.x.x.x"

incp_port=6669

incp_user=""

incp_passwd=""

public_user="public"
##### 说明:

select_limit 和 export_limit为系统默认查询和导出条数限制

incp_XX系列配置文件为inception的连接配置

#### setttings.py中的修改内容主要为mysql、redis地址，以及邮件服务器相关地址
### 启动：
#### 初始化表结构： python manage.py migrate
#### 创建一个超级用户： python manage.py createsuperuser
#### 启动server： 

python manage.py runserver 0.0.0.0:8000（启动前建议把settings.py中的debug设置为false） 

(上面的启动方式可以自己测试时使用，实际使用不要使用django自带的server启动，因为好像是单线程在处理request的。。用apache或别的方式启动)

##### 然后以刚刚注册的超级用户登陆网站进行建立普通用户、建库等配置工作

### 定时任务配置
#### 在django库中导入mon_tb.sql
#### 启用celery的定时任务功能: python manage.py celery beat 
#### 启动celery:  python manage.py celery worker -E -c 3 --loglevel=info 
#### 开启快照监控后，在admin中能看到任务，默认一秒一个快照: python manage.py celerycam 
#### 在/admin/中设置定时任务
##### 设置定时扫描task
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/crontab_sche.jpg)
##### 设置元数据收集任务
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/crontab_tbcheck.jpg)


# 页面展示大致如下:
## 1.登录界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/login.jpg)
## 2.主页
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/main.jpg)
## 3.表结构查询界面
支持表名模糊搜索
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/meta_query.jpg)
### 3.2查询结果:
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/meta_info.jpg)
## 4.查询界面
### 4.1表查询:
支持单条sql的查询和查询结果的导出，导出条数限制默认为config.py中配置的值，也可以通过后台myapp_profile表对特定用户进行调整
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/mysql_query.jpg)
## 5.执行界面
支持单条sql语句的执行，用户能够执行的语句类型可以通过权限限制。
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/mysql_exec.jpg)
## 6.任务提交界面

只有审核通过的sql，才能被提交至任务管理页面

![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/task_upload.jpg)
## 7.任务管理界面
可以审核、查看、修改、执行、预约任务执行时间，通过调用inception接口来实现

不同用户能够看到的页面按钮可以通过权限控制

任务界面如下：

点击执行后，任务会被发送给celery后台异步执行，通过点击状态按钮查看任务执行状态

可以配置邮件在任务生成和任务结束时候发送邮件告知相关人员

可以导出csv格式任务，支持utf8和gb18030两种导出格式

![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/task_manage1.jpg)
### 7.1任务执行结果示例
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/resul_of_task.jpg)
### 7.2 任务终止
通过pt-osc执行的任务

通过inception调用pt-osc执行的任务可以被终止，但停止后需要到库中人工清理触发器
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/task_stop_ptosc.jpg)
未通过pt-osc执行的任务
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/task_stop.jpg)

### 7.3 任务编辑界面
可以通过权限设置来限制用户是否能够编辑此页面的内容

可以单独变更执行的数据源，以实现同一语句在不同环境执行的需求

变更数据源后，会新生成一个任务，并发送邮件告知
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/task_edit_1.jpg)
## 8.日志查询界面
本平台记录所有用户在mysql_query,mysql_exec以及任务管理页面中执行的语句

这些语句可以通过日志查询页面进行搜索

![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/oper_log.jpg)
## 9. 数据库管理界面
#### 使用页面功能需要配置role为admin的数据库账号

![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/mysql_admin.jpg)
#### 此页面数据由crontab任务收集信息得到
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/mysql_admin1.jpg)

## 10.权限查询页面示例
### 10.1按db查询
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/pre_query_db.jpg)
### 10.2按db组查询
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/pre_query_dbgroup.jpg)
### 10.3按用户账号查询
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/pre_query_user.jpg)
### 10.4按实例查询
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/pre_query_ins.jpg)
## 11.用户账户设置界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/user_set.jpg)
## 12.DB快速创建界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/fast_dbset.jpg)
## 13.DB详细设置界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/db_detailset.jpg)
## 14.用户页面权限设置界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/group_set.jpg)
## 15.DB组设置界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/dbgroup_set.jpg)
## 16.用户密码自助重置页面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/pass_reset.jpg)

### 个人编写，精力和水平有限。。有任何疑问和建议联系 changjingxiu1@163.com
