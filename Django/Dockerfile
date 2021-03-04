# Pull the base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY cert.pem /etc/cert.pem
COPY privkey.pem /etc/privkey.pem
#RUN mkdir /code
#COPY . /code/
#WORKDIR /code
#Upgrade pip
RUN pip install --default-timeout=100 pip -U

RUN apt-get update --allow-releaseinfo-change -y

RUN apt-get install python3-pymysql -y
#Install dependencies
#RUN pip install --default-timeout=100 -r requirements.txt
#RUN pip install  -r requirements.txt --upgrade

# Add wait-for-it


# Put COPY steps at the end for faster speed

RUN mkdir /code
COPY . /code/

WORKDIR /code

#RUN pip install --default-timeout=100 -r requirements.txt
RUN pip install  -r requirements.txt --upgrade

