FROM python:3.6
MAINTAINER Justin Phillips "justin_phillips@ultimatesoftware.com"
# Create the group and user to be used in this container
RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask
ADD . /app
COPY ./src/ /app/
COPY ./requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
RUN chown -R flask:flaskgroup /home/flask
USER flask