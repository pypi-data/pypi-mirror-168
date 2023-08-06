# Airflow connections manager

Interface to access Airflow connections. Actually it works in Airflow environments with the API enabled with Basic Authentication

## Usage

You must have the following environment variables declared
```
AIRFLOW_API_URL=<your Airflow API url like http://localhost:8080/api/v1>
AIRFLOW_API_TOKEN=<your Airflow Basic Auth token like Basic YXRtaW46YHRt8W4=>
```

Sample
```
from airflow_connections_manager import AirflowConnectionsManager

connections = AirflowConnectionsManager.list_connections()
```

## Building for PyPi deployment

https://packaging.python.org/en/latest/tutorials/packaging-projects/
```
python -m pip install --upgrade build

python -m build

python -m twine upload --repository testpypi dist/*
```