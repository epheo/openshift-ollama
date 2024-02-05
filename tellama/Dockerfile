FROM ubi9

RUN dnf -y install python-pip
RUN pip install requests python-telegram-bot

ADD ./tellama.py .

CMD python3 tellama.py
