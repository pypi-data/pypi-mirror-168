import json
import os

import requests


class AirflowApiClient:
    def __init__(self):
        self.base_url = os.getenv("AIRFLOW_API_URL", None)
        self.auth_token = os.getenv("AIRFLOW_API_TOKEN", None)

    def do_request(self, method, url, data=None):
        headers = {"Authorization": self.auth_token, "Content-Type": "application/json"}

        if data is not None:
            data = json.dumps(data)

        resp = requests.request(method, url=f"{self.base_url}/{url}", data=data, headers=headers)

        if resp.status_code != 200:
            raise Exception(f"Airflow API error with detail: {str(resp.raise_for_status())}")
        return resp.json()

    def list_connections(self):
        return self.do_request("GET", "connections")

    def create_db_connection(self, data: dict):
        conn = {
            "connection_id": data["connectionId"],
            "conn_type": "generic",
            "host": data["host"],
            "port": int(data["port"]),
            "login": data["username"],
            "password": data["password"],
            "schema": data["database"],
        }

        return self.do_request("POST", "connections", conn)

    def create_generic_connection(self, data: dict):
        conn = {"connection_id": data["connectionId"], "conn_type": "generic", "extra": data["extra"]}
        return self.do_request("POST", "connections", conn)

    def create_connection(self, data: dict):
        if data["connectionType"] == "database":
            return self.create_db_connection(data)
        return self.create_generic_connection(data)

    def get_connection(self, conn_id):
        return self.do_request("GET", f"connections/{conn_id}")

    def delete_connection(self, conn_id):
        return self.do_request("DELETE", f"connections/{conn_id}")
