FROM python:3.8

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ワーキングディレクトリを設定
WORKDIR /code

# 依存関係をinstall
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# projectのsource codeをcopy
COPY ./pongproject .
#RUN cd ./pongproject/