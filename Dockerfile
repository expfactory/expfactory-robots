FROM ubuntu:16.04

# docker build -t vanessa/expfactory-robots .

RUN apt-get update && apt-get install -y git wget python3-pip \
                   python3-dev xvfb libfontconfig fonts-liberation \
                   gconf-service libappindicator1 libasound2 libnspr4 \
                   libnss3 libxss1 lsb-release xdg-utils
WORKDIR /opt 
RUN git clone https://www.github.com/expfactory/expfactory
RUN wget "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
WORKDIR expfactory 
RUN python3 setup.py install
RUN python3 -m pip install selenium pyvirtualdisplay

# Install Chrome
WORKDIR /opt
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt-get -f install
RUN apt-get install -y -f
RUN rm google-chrome-stable_current_amd64.deb

RUN mkdir /code  # for script
WORKDIR /code
ADD . /code
RUN chmod u+x /code/start.py
RUN mkdir /data  # bind experiment folder to
RUN apt-get clean

ENTRYPOINT ["xvfb-run", "python3", "/code/start.py"]
