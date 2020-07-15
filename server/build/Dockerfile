FROM python:3.7-slim
COPY oss.py /oss.py
RUN pip install tornado==5.1.1 && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ENTRYPOINT ["python3","oss.py"]