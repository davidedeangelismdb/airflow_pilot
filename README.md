# airflow_pilot
* clone airflow_pilot
# run aiurflow_pilot
* minikube start
* eval $(minikube docker-env)
* docker build -t airflow-local .
* kubectl apply -f environments/local.yml
* kubectl get pods
* kubectl expose deployment airflow-local --type=NodePort
* minikube service airflow-local --url
# LOGS
kubectl logs airflow-local-7f8f8b5f5f-8cn7p
# SH 
kubectl exec -it airflow-local-7f8f8b5f5f-8cn7p -- /bin/sh
# DELETE DEPLOYMENT
kubectl delete deployment airflow-local
