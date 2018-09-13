FROM airflow-local-prereq

#don't load the airflow examples
ENV AIRFLOW__CORE__LOAD__EXAMPLES=False

RUN mkdir -p /home/root/airflow/karakurilogs

#copy the dags
RUN mkdir -p /home/root/airflow/dags
COPY dags /home/root/airflow/dags/

#copy the mong_plugin
RUN mkdir -p /home/root/airflow/plugins/mongo_plugin
COPY mongo_plugin /home/root/airflow/plugins/mongo_plugin

#copy requirements for the plugin and install them
COPY requirements.txt /home/root/airflow
RUN pip3 install -r /home/root/airflow/requirements.txt

RUN mkdir -p /home/root/pyforce
COPY pyforce /home/root/pyforce
RUN pip3 install -e /home/root/pyforce

RUN mkdir -p /home/root/support-tools-libs
COPY support-tools-libs /home/root/support-tools-libs
RUN pip3 install -e /home/root/support-tools-libs


#to review due to dependencies errors
RUN pip3 install apache-airflow[crypto]


#UNCOMMENT FOR USING POSTGRES DB
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://postgresadmin:admin123@192.168.99.101:30955/postgres
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__LOGGING__LEVEL=DEBUG
ENV AIRFLOW__CORE__FERNET_KEY=GOrDnxFGGb0CHCmxjmyZ298PI7CVOuLpuOTGb2Kpld4=

# initialize the database
RUN airflow initdb

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the service when the container launches
CMD ["sh", "-c", "airflow webserver -p 80"]


