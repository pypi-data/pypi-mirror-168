from airflow_api_client import AirflowApiClient


class AirflowConnectionsManager:
    api_client = AirflowApiClient()

    @staticmethod
    def list_connections() -> list:
        """Lists all connections

        Returns:
        list: List of dicts with properties connection_id and value (not visible)

        """
        conns = None
        try:
            conns = AirflowConnectionsManager.api_client.list_connections()
        except Exception as error:
            return error

        output = []
        connections = conns["connections"]

        if connections is not None and len(connections) > 0:
            for item in connections:
                output.append({"connection_id": item["connection_id"], "value": "*****"})
        return output

    @staticmethod
    def get_connection(conn_id: str) -> dict:
        """Obtains a connection by ID

        Parameters:
        conn_id (str): Unique conncetion identifier

        Returns:
        dict: Dictionary with connection details

        """
        conn = None
        try:
            conn = AirflowConnectionsManager.api_client.get_connection(conn_id)
        except Exception as error:
            return error

        output = None

        if conn["extra"] is not None:
            return conn["extra"]
        else:
            output = {}
            output["host"] = conn["host"]
            output["port"] = conn["port"]
            output["database"] = conn["schema"]
            output["username"] = conn["login"]
        return output

    @staticmethod
    def delete_connection(conn_id: str) -> str:
        """Deletes a connection by ID

        Parameters:
        conn_id (str): Unique conncetion identifier

        Returns:
        str: Success message

        """
        try:
            AirflowConnectionsManager.api_client.delete_connection(conn_id)
        except Exception as error:
            return error
        return f"Successfully deleted secret with id {conn_id}"

    @staticmethod
    def create_db_connection(conn_id: str, host: str, port: int, database: str, username: str, password: str) -> str:
        """Creates a database connection

        Parameters:
        conn_id (str): Unique conncetion identifier
        host (str): Database host
        port (int): Database port
        database (str): Database name
        username (str): Username
        password (str): Password

        Returns:
        str: Success message

        """
        data = {
            "connectionId": conn_id,
            "host": host,
            "port": int(port),
            "database": database,
            "username": username,
            "password": password,
        }
        try:
            AirflowConnectionsManager.api_client.create_db_connection(data)
        except Exception as error:
            return error
        return f"Successfully created database connection with id {conn_id}"

    @staticmethod
    def create_generic_connection(conn_id: str, data: dict) -> str:
        """Creates a generic connection

        Parameters:
        conn_id (str): Unique conncetion identifier
        data (dict): Dict with data (ex.: json.dumps({"apiKey": "123"}))

        Returns:
        str: Success message

        """
        input_data = {"connectionId": name, "extra": data}
        try:
            AirflowConnectionsManager.api_client.create_generic_connection(input_data)
        except Exception as error:
            return error
        return f"Successfully created generic connection with id {name}"
