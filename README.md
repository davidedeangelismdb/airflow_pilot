# airflow_pilot
* clone airflow_pilot
* cd airflow_pilot
* clone inside pyforce
  git clone --branch feature/python3 git@github.com:thiagogalesi/pyforce.git
* close support-tools-libs
  git clone --branch staging git@github.com:10gen/support-tools-libs.git
# run aiurflow_pilot
* minikube start
* eval $(minikube docker-env)
* docker build -t airflow-local-prereq -f Dockerfile.prereq .
* docker build -t airflow-local-app -f Dockerfile.app .
* kubectl apply -f environments/local.yml
* kubectl get pods
* kubectl expose deployment airflow-local-app --type=NodePort
* minikube service airflow-local-app --url
# LOGS
kubectl logs airflow-local-app-7f8f8b5f5f-8cn7p
# SH 
kubectl exec -it airflow-local-app-7f8f8b5f5f-8cn7p -- /bin/sh
# DELETE DEPLOYMENT
kubectl delete deployment airflow-local-app
# run this command for scheduling the dags
airflow scheduler

# POSTGRES CREATION
* kubectl create -f postgres/postgres-configmap.yaml
* kubectl create -f postgres/postgres-storage.yaml
* kubectl create -f postgres/postgres-deployment.yaml
* kubectl create -f postgres/postgres-service.yaml
* kubectl get svc postgres
* minikube service postgres --url
* psql -h 192.168.99.100 -U postgresadmin --password -p 31192 postgresdb
# Operate on the database server
* \l # List all databases
* \du # List all users/roles
* \dt # Show all tables in database
* \h # List help information
* \q # Quit the prompt
# Create a meta db for airflow
* CREATE DATABASE airflow;
* \l # Check for success

# POSTGRES DELETION
* kubectl delete service postgres 
* kubectl delete deployment postgres
* kubectl delete configmap postgres-config
* kubectl delete persistentvolumeclaim postgres-pv-claim
* kubectl delete persistentvolume postgres-pv-volume