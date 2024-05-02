FROM ubuntu

RUN mkdir /liq_bot/
COPY ./* /liq_bot/

ENV bot_home /liq_bot

# 添加国内apt源 (此处有bug)
#COPY ./sources.list /etc/apt/s2.list
#RUN cat /etc/apt/s2.list /etc/apt/sources.list > /etc/apt/sources.list
#RUN rm /etc/apt/s2.list

RUN apt update
RUN apt install make -y
RUN apt install colorized-logs -y
RUN apt install python3 python3-pip -y

# 设置pip国内源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install lottie cairosvg

WORKDIR ${bot_home}

RUN chmod +x ./*.sh && chmod +x ./*.py

RUN ./init.sh
RUN ./mt_run.sh
RUN make
