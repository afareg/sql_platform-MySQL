# sql_manage_platform-MySQL
## 基于django和inception，带权限控制的mysql语句运行系统
### 开发环境：
#### django:1.8.14
#### python:2.7.12
### python依赖组件：
#### django-crontab
#### django-simple-captcha
#### django-sslserver
#### django-ratelimit
#### MySQL-python

### 启动配置
#### config.ini配置文件如下：
[settings]
host="127.0.0.1" 
port=3306
user="xx"
passwd="xxx"
dbname="xxx"
wrong_msg="select '请检查输入语句'"
select_limit=200
export_limit=200
incp_host="x.x.x.x"
incp_port=6669
incp_user=""
incp_passwd=""
public_user="public"
##### 说明:
host-dbname为django库的连接配置，和settings.py中的一致即可
select_limit 和 export_limit为系统默认查询和导出条数限制
incp_XX系列配置文件为inception的连接配置
#### 定时任务配置
修改seheduled.py中第18行路径地址为正确地址
config.readfp(open('/root/PycharmProjects/mypro/myapp/etc/config.ini','r'))
然后运行 python manage.py crontab add 添加 crontab任务

### 启动：
#### python manage.py runsslserver 0.0.0.0:8000

## 1.登录界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/login.jpg)
## 2.主页
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/main.jpg)
## 3.表结构查询界面
### 3.1表查询:
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/meta_query.jpg)
### 3.2查询结果:
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/meta_info.jpg)
## 4.查询界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/mysql_query.jpg)
## 5.执行界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/mysql_exec.jpg)
## 6.任务提交界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/task_upload.jpg)
## 7.任务管理界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/task_manage.jpg)
### 7.1任务执行结果示例
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/resul_of_task.jpg)
### 7.2任务编辑界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/task_edit.jpg)
## 8.日志查询界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/oper_log.jpg)
## 9.权限查询页面示例
### 9.1按db查询
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/pre_query_db.jpg)
### 9.2按db组查询
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/pre_query_dbgroup.jpg)
### 9.3按用户账号查询
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/pre_query_user.jpg)
### 9.4按实例查询
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/pre_query_ins.jpg)
## 10.用户账户设置界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/user_set.jpg)
## 11.DB快速创建界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/fast_dbset.jpg)
## 12.DB详细设置界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/db_detailset.jpg)
## 13.用户页面权限设置界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/group_set.jpg)
## 14.DB组设置界面
![image](https://github.com/speedocjx/myfile/blob/master/sql-manage-platform/dbgroup_set.jpg)
