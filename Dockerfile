FROM ubuntu:latest

# install Python 3
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "application.py" ]
