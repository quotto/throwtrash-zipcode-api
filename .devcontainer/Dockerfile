FROM python:3.8-buster

RUN apt update -y && apt install -y zip unzip
RUN pip install --upgrade pip && pip install pipenv
ENV PIPENV_VENV_IN_PROJECT true
# Pylintでのパス解決のために設定
ENV PYTHONPATH ..
# pipenv用の設定
ENV PIPENV_TIMEOUT=1800
ENV PIPENV_INSTALL_TIMEOUT=1800

# aws cliの導入
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

WORKDIR /workspaces