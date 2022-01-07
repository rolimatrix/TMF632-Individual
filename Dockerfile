FROM mtr.external.otc.telekomcloud.com/digitalhub/python3:master

# We copy just the requirements.txt first to leverage Docker cache
COPY /requirements.txt /app/requirements.txt
WORKDIR /app

ENV PYTHONUNBUFFERED=1
RUN apk add --update build-base && \
    apk add --no-cache gcc musl-dev postgresql-dev && \
    python3 -m ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools && \
    pip install -r /app/requirements.txt
    
COPY . /app
RUN ls -la /app
EXPOSE 8080
ENTRYPOINT [ "python" ]
CMD [ "/app/app.py" ]
