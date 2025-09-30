FROM mcr.microsoft.com/devcontainers/python:0-3.11

LABEL MAINTAINER="Fedorov"

# 生成docker-compose时候使用
COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --upgrade pip && pip3 config set global.index-url https:\/\/pypi.tuna.tsinghua.edu.cn\/simple
RUN pip3 install -r /tmp/requirements.txt
# 添加证书
RUN pip3 install certifi && \
       echo "export REQUESTS_CA_BUNDLE=$(python -c 'import certifi; print(certifi.where())')" >> /etc/profile

# 设置 HTTP 和 HTTPS 代理
# ENV HTTP_PROXY=http://10.178.34.133:7890
# ENV HTTPS_PROXY=http://10.178.34.133:7890
# ENV NO_PROXY=localhost,127.0.0.1

EXPOSE 7070

# CMD ["streamlit", "run", "main.py","--server.port 8888"]