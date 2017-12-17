FROM ubuntu:16.04

# docker build -t vanessa/expfactory-robots .

RUN apt-get update && apt-get install -y git python3-pip python3-dev
WORKDIR /opt 
RUN git clone https://www.github.com/expfactory/expfactory
WORKDIR expfactory 
RUN python3 setup.py install
RUN python3 -m pip install pandas

RUN mkdir /code  # for script
WORKDIR /code
ADD . /code
RUN chmod u+x /code/start.py
RUN mkdir /data  # bind experiment folder to
RUN apt-get clean

ENTRYPOINT ["python3", "/code/start.py"]
