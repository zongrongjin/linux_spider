#Python3作为基础映像
FROM python:3.7
#设置环境变量,使用which Python可以查看
ENV PATH=/usr/local/bin:$PATH
#添加当前目录到容器里
ADD . /code
#设置容器工作路径
WORKDIR /code
#安装Python插件
RUN pip install -r requirements.txt
#设置容器工作目录
WORKDIR /code/ershouche/
#运行命令
CMD /usr/local/bin/scrapy crawlall
#暴露端口
EXPOSE 22