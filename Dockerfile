FROM python:3.8

ADD ./app.py /
ADD ./wait-for-it.sh /

RUN pip install cryptography numpy pandas python-binance sqlalchemy pymysql

RUN chmod +x /wait-for-it.sh

CMD ["./wait-for-it.sh", "mysql:3306", "--", "python", "./app.py"]