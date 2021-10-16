FROM mtr.external.otc.telekomcloud.com/dboeck/roliimage:latest
#FROM python:3.9
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["sh","-c","echo 'Hello Roland' && pip3 freeze && python3 /app/app.py"]
#CMD ["python", "/app/app.py"]
#CMD ["sh","-c","python3 /app/app.py"]