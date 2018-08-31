FROM airflow-local-prereq

#don't load the airflow examples
ENV AIRFLOW_CORE_LOAD_EXAMPLES=False

#copy the dags
RUN mkdir -p /home/root/airflow/dags
COPY dags /home/root/airflow/dags/

#copy the mong_plugin
RUN mkdir -p /home/root/airflow/plugins/mongo_plugin
COPY mongo_plugin /home/root/airflow/plugins/mongo_plugin

#copy requirements for the plugin and install them
COPY requirements.txt /home/root/airflow
RUN pip3 install -r /home/root/airflow/requirements.txt

#to review due to dependencies errors
RUN pip3 install apache-airflow[crypto]

# initialize the database
RUN airflow initdb

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the service when the container launches
CMD ["sh", "-c", "airflow webserver -p 80"]


