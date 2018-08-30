FROM alpine:3.6

RUN apk add --no-cache python3 python3-dev musl-dev util-linux linux-headers openssl-dev openssl git g++ libxml2-dev libxslt-dev gcc libffi libffi-dev sudo

ENV AIRFLOW_HOME ~/airflow

ENV SLUGIFY_USES_TEXT_UNIDECODE yes

# install from pypi using pip
RUN pip3 install apache-airflow

# initialize the database
RUN airflow initdb

# start the web server, default port is 8080
#RUN airflow webserver -p 8080

# visit localhost:8080 in the browser and enable the example dag in the home page

# Make port 80 available to the world outside this container
EXPOSE 80

# Placeholder for a prepare script (per service)

# Run the service when the container launches
CMD ["sh", "-c", "airflow webserver -p 80"]