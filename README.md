# Standard

#### 介绍
- 1.支持通信协议加密协议 RSA+AES+其他
- 2.支持基于 pytorch 训练Rnn 模型
- 3.支持基于金融模型ARIMA进行模型预测
- 5.支持认证中间件
- 6.支持限流中间件
- 7.支持rbac用户角色权力管理
- 8.分页库
- 9.数据库采用redis,mysql(sqlite3)
### 拉取
```
    git clone https://github.com/jackerzz/Standard.git
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