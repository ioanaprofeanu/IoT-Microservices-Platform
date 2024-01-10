from datetime import datetime, timezone, timedelta
from dateutil import parser
import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import os

# get the environment variables
db_name = os.environ.get('DB_NAME')
debug_data_flow = os.environ.get('DEBUG_DATA_FLOW')
mosquitto_host = os.environ.get('MOSQUITTO_HOST')
influxdb_host = os.environ.get('INFLUXDB_HOST')

# function for printing debug messages


def log_debug_data_flow(msg):
    # print only if the env variable is set to True
    if debug_data_flow == "True":
        print(msg)

# function for parsing and verifying the topic format


def parse_topic(topic):
    # verify if the topic contains '/'
    if '/' not in topic:
        return None, None

    # split the topic by '/' delimiter and retrieve the parts
    parts = topic.split('/')

    # there must be 2 parts (location/station)
    if len(parts) != 2:
        return None, None

    # return the location and station
    return parts[0], parts[1]

# function for verifying if a given payload is a valid JSON


def is_valid_json(json_str):
    try:
        loaded_object = json.loads(json_str)
        return isinstance(loaded_object, (dict, list))
    except json.JSONDecodeError:
        return False

# function for handling the adaptor connection to the broker


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log_debug_data_flow("Adapter connected successfully.")
        # subscribe to all topics
        client.subscribe("#")
    else:
        log_debug_data_flow(f"Failed to connect adapter with code {rc}.")


# function for handling message receival
def on_message(client, userdata, msg, influxdb_client):
    log_debug_data_flow(f"Received a message by topic [{msg.topic}]")

    # get the location and station from the topic and verify if they are valid
    location, station = parse_topic(msg.topic)

    if location is None or station is None:
        log_debug_data_flow(
            "ERROR: Invalid topic format. Expected format: location/station.")
        return

    # verify if the payload is a valid JSON
    if (is_valid_json(msg.payload.decode()) == False):
        log_debug_data_flow("ERROR: Invalid payload JSON format.")
        return

    # extract the payload from the message
    payload = json.loads(msg.payload)

    # check if the payload["timestamp"] exists in the payload
    if "timestamp" in payload:
        # convert the timestamp to the ISO format
        timestamp_object = parser.parse(payload['timestamp'])
        timestamp = timestamp_object.strftime("%Y-%m-%dT%H:%M:%S%z")
        payload['timestamp'] = timestamp
        log_debug_data_flow(f"Data timestamp is: {payload['timestamp']}")
    else:
        # if the timestamp does not exist, set it to the current time
        log_debug_data_flow(f"Data timestamp is: NOW")
        timestamp = datetime.now(timezone(timedelta(hours=3))).isoformat()
        payload['timestamp'] = timestamp

    # create the to be inserted datapoints using the payload
    datapoints = []
    for key in payload:
        # if payload[key] is int or float
        if isinstance(payload[key], int) or isinstance(payload[key], float):
            log_debug_data_flow(f"{location}.{station}.{key} {payload[key]}")
            # create the datapoint
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

    # write the datapoints to the database
    if (len(datapoints) > 0):
        influxdb_client.write_points(datapoints)


def main():
    # connect to the InfluxDB database
    influxdb_client = InfluxDBClient(host=influxdb_host)

    # check if the database exists
    database_list = influxdb_client.get_list_database()
    if any(db['name'] == db_name for db in database_list):
        # switch to the already existing database
        influxdb_client.switch_database(db_name)
    else:
        # create the database
        influxdb_client.create_database(db_name)
        influxdb_client.switch_database(db_name)

    # connect to the broker
    mosquitto_client = mqtt.Client()
    mosquitto_client.on_connect = on_connect
    mosquitto_client.on_message = lambda client, userdata, msg: on_message(
        client, userdata, msg, influxdb_client)
    mosquitto_client.connect(mosquitto_host)
    mosquitto_client.loop_forever()


if __name__ == "__main__":
    main()
