FROM python:3.6
MAINTAINER Justin Phillips "justin_phillips@ultimatesoftware.com"
ADD . /app
COPY ./src /app
COPY ./requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]