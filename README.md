# Standard

#### 介绍

### 拉取
```
    git clone https://github.com/jackerzz/FastapiWebSocekt.git
```
### 安装
- 1.环境依赖
    - python3.7
    - pip3

- 2.安装依赖
``` 
    virtualenv venv
    source venv/Scripts/activate
    pip install -r requirements.txt -i https://pypi.doubanio.com/simple

    # 更新依赖
         pip freeze > requirements.txt
```

#### 项目组件的使用
1. 中间件：
    1. 认证中间件
    2. 限流中间件
    3. rbac 权限认证
    
2. 库：
    1. 分页库
    2. 工具库

###### makemigrations
为项目创建一个新的迁移
```shell
cd ./Standard
python manage.py makemigrations
```

###### migrate
将迁移应用到数据库
```shell
cd ./Standard
python manage.py migrate
```

###### runserver
启动一个web服务
```shell
cd ./Standard
python manage.py runserver
```
Options:  
-h, --host　　　　　[default:127.0.0.1]  
-p, --port　　　　　[default:8000]  
-w, --workers　　　[default:1]  
--reload　　　　　　auto-reloader  