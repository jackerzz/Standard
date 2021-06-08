
# Standard

#### 介绍
基于 fastapi-manage 工具生成的
fastapi的模板生成，数据库版本管理工具   
fastapi+sqlalchemy  
此项目包含了模板目录(./templates)和模板应用工具(./serializer.py) 提供给开发者自行定制修改的一个工具

### 安装依赖
```shell
virtualenv venv
pip install fastapi-manage
```

#### 使用说明

1.  templates 存放着模板文件
    - 支持开发者修改自定义模型
2.  serializer.py 负责将模板文件写入到main.py中，成为一个变量 
    - 支持开发者进行修改或开发新的模板
3.  conf.py 里包含可配置的模板参数
4.  main 负责提供所有功能，创建项目，执行迁移等等
#### 项目组件的使用
1. 中间件：
    1. 认证中间件
    2. 限流中间件
    
2. 库：
    1. 分页库
    2. 工具库

#### fastapi-manage的使用
##### 安装
```shell
pip install fastapi-manage
```
##### 使用
###### startproject
在当前目录下创建一个fastapi项目， 目录名为当前输入的项目名
```shell
fastapi-manage startproject yourproject
```

###### makemigrations
为项目创建一个新的迁移
```shell
cd ./yourproject
python manage.py makemigrations
```

###### migrate
将迁移应用到数据库
```shell
cd ./yourproject
python manage.py migrate
```

###### runserver
启动一个web服务
```shell
cd ./yourproject
python manage.py runserver
```
Options:  
-h, --host　　　　　[default:127.0.0.1]  
-p, --port　　　　　[default:8000]  
-w, --workers　　　[default:1]  
--reload　　　　　　auto-reloader  
##### 启动异常
- start-celery.sh
```
    问题：
        ModuleNotFoundError: No module named 'grp'
    解决：
        pip install celery==5.0.5
```