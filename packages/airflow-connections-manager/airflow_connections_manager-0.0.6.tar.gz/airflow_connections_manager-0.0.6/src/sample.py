import json

from airflow_connections_manager import AirflowConnectionsManager


# connections = AirflowConnectionsManager.list_connections()
# print(connections)

# connection = AirflowConnectionsManager.get_connection("test_123")
# print(connection)

"""
create = AirflowConnectionsManager.create_db_connection(
	"test_123",
	"127.0.0.1",
	5432,
	"my_db",
	"my_user",
	"my_passwd"
)
print(create)
"""
# connection = AirflowConnectionsManager.get_connection("test_123")
# print(connection)

# AirflowConnectionsManager.delete_connection("test_123")

"""
create_generic = AirflowConnectionsManager.create_generic_connection(
	"my_generic",
	json.dumps({"apiKey": "aaBBCCddFFgg"})
)
print(create_generic)
"""

# connection = AirflowConnectionsManager.get_connection("my_generic")
# print(connection)
