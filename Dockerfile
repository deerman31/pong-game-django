FROM debian:11

# wordPressと連携するためのPHPといくつかの拡張機能、mysqlとの連携に必要なphp-mysqli、CURL、GDライブラリなどをインストール。
RUN apt-get update -y && apt-get install python \

COPY ./requirements.txt ./requirements.txt

RUN chmod +x /bin/wordpress_setup.sh

ENTRYPOINT ["wordpress_setup.sh" ]