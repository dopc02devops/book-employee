import os

POSTGRES_PORT = '5432'
SECRETS = 'somethingunique'
# local db
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'Simon1980'
POSTGRES_HOST = 'localhost'
POSTGRES_DB = 'flaskdb'
POSTGRES = 'postgresql'

# Retrieve PostgreSQL connection details from environment variables
username = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
database = os.getenv('POSTGRES_DB')
minikube_host = os.getenv('POSTGRES_HOST_minikube')

KUBERNETES_DB = f'{POSTGRES}://{username}:{password}@{host}:{port}/{database}'

MINIKUBE_DB = f'{POSTGRES}://{username}:{password}@{minikube_host}/{database}'

LOCAL_DB = f'{POSTGRES}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
