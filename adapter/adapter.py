from datetime import datetime, timezone, timedelta
import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import os

db_name = os.environ.get('DB_NAME')
debug_data_flow = os.environ.get('DEBUG_DATA_FLOW')
mosquitto_host = os.environ.get('MOSQUITTO_HOST')
influxdb_host = os.environ.get('INFLUXDB_HOST')

def log_debug_data_flow(msg):    
    if debug_data_flow == "True":
        print(msg)


def parse_topic(topic):
    # Check if the topic follows the expected format
    if '/' not in topic:
        log_debug_data_flow("ERROR: Invalid topic format. Expected format: location/station.")
        return None, None

    # Split the topic using the '/' delimiter
    parts = topic.split('/')

    # Check if there are exactly two parts
    if len(parts) != 2:
        log_debug_data_flow("ERROR: Invalid topic format. Expected format: location/station.")
        return None, None

    # Assign values to station and location
    location = parts[0]
    station = parts[1]

    return location, station


def is_valid_json(json_str):
    try:
        loaded_object = json.loads(json_str)
        return isinstance(loaded_object, (dict, list))
    except json.JSONDecodeError:
        return False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log_debug_data_flow("Adapter connected successfully.")
        client.subscribe("#")
    else:
        log_debug_data_flow(f"Failed to connect adapter with code {rc}.")


def on_message(client, userdata, msg, influxdb_client):
    log_debug_data_flow(f"Received a message by topic [{msg.topic}]")

    location, station = parse_topic(msg.topic)

    if (is_valid_json(msg.payload.decode()) == False):
        log_debug_data_flow("ERROR: Invalid payload JSON format.")
        return

    payload = json.loads(msg.payload)

    # get each value from payload in an if
    # check if the payload["timestamp"] exists in the payload
    if "timestamp" in payload:
        log_debug_data_flow(f"Data timestamp is: {payload['timestamp']}")
    else:
        log_debug_data_flow(f"Data timestamp is: NOW")
        timestamp = datetime.now(timezone(timedelta(hours=3))).isoformat()
        payload['timestamp'] = timestamp

    datapoints = []
    for key in payload:
        # if payload[key] is int or float
        if isinstance(payload[key], int) or isinstance(payload[key], float):
            log_debug_data_flow(f"{location}.{station}.{key} {payload[key]}")
            data_point = {
                "measurement": station + "." + key,
                "tags": {
                    "location": location,
                    "station": station
                },
                "time": payload['timestamp'],
                "fields": {
                    "value": payload[key]
                }
            }
            datapoints.append(data_point)

    if (len(datapoints) > 0):
        influxdb_client.write_points(datapoints)


def main():
    influxdb_client = InfluxDBClient(host=influxdb_host)

    database_list = influxdb_client.get_list_database()
    if any(db['name'] == db_name for db in database_list):
        # Database exists, switch to it
        influxdb_client.switch_database(db_name)
    else:
        # Database does not exist, create it
        influxdb_client.create_database(db_name)
        influxdb_client.switch_database(db_name)

    mosquitto_client = mqtt.Client()
    mosquitto_client.on_connect = on_connect
    mosquitto_client.on_message = lambda client, userdata, msg: on_message(
        client, userdata, msg, influxdb_client)  # Pass influxdb_client as a parameter

    mosquitto_client.connect(mosquitto_host)
    mosquitto_client.loop_forever()


if __name__ == "__main__":
    main()
