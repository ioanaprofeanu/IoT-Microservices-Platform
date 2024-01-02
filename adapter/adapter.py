from datetime import datetime, timezone, timedelta
import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import time

# TODO: creeaza env var
iot_data = "iot_data"


def parse_topic(topic):
    # Check if the topic follows the expected format
    if '/' not in topic:
        print("Invalid topic format. Expected format: location/station.")
        return None, None

    # Split the topic using the '/' delimiter
    parts = topic.split('/')

    # Check if there are exactly two parts
    if len(parts) != 2:
        print("Invalid topic format. Expected format: location/station.")
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
        print("Adapter connected successfully.")
        client.subscribe("#")
    else:
        print(f"Failed to connect adapter with code {rc}.")


def on_message(client, userdata, msg, influxdb_client):
    # TODO: DE ADAUGAT DEBUT MESSAGES CAND AM VAR DE MEDIU SETATA PE TRUE; inlocuieste print cu logging
    print(f"TOPIC {msg.topic}: {msg.payload.decode()}")

    location, station = parse_topic(msg.topic)

    if (is_valid_json(msg.payload.decode()) == False):
        print("Invalid payload JSON format.")
        return

    payload = json.loads(msg.payload)

    # get each value from payload in an if
    # check if the payload["timestamp"] exists in the payload
    if "timestamp" in payload:
        print(f"timestamp: {payload['timestamp']}")
    else:
        timestamp = datetime.now(timezone(timedelta(hours=3))).isoformat()
        payload['timestamp'] = timestamp
        # de egnerat automat temp pe adaptor
        print("timestamp not found in payload.")
        print(f"new generated timestamp: {payload['timestamp']}")

    datapoints = []
    for key in payload:
        # if payload[key] is int or float
        if isinstance(payload[key], int) or isinstance(payload[key], float):
            print(f"{key}: {payload[key]}")
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
        # print datapoints
        print(datapoints)
        print("Data points written to InfluxDB.")


def main():
    influxdb_client = InfluxDBClient(host='localhost', port=8086)

    database_list = influxdb_client.get_list_database()
    if any(db['name'] == iot_data for db in database_list):
        # Database exists, switch to it
        influxdb_client.switch_database(iot_data)
        print(f"Switched to existing database: {iot_data}")
    else:
        # Database does not exist, create it
        influxdb_client.create_database(iot_data)
        influxdb_client.switch_database(iot_data)
        print(f"Created and switched to new database: {iot_data}")

    mosquitto_client = mqtt.Client()
    mosquitto_client.on_connect = on_connect
    mosquitto_client.on_message = lambda client, userdata, msg: on_message(
        client, userdata, msg, influxdb_client)  # Pass influxdb_client as a parameter

    mosquitto_client.connect("localhost", 1883)
    mosquitto_client.loop_forever()


if __name__ == "__main__":
    main()
