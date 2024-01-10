# IOT-Microservices-Platform
## Profeanu Ioana, 343C1 - Tema3 SPRC

## Project run:
- ./run.sh (it is possible to need rights to execute - chmod a+x ./run.sh) - it builds and deploys
the docker services stack
- docker stack rm sprc3 - for removing the stack
- docker swarm init - this command must have been run initially, in order to initialize a docker
swarm
- docker service logs sprc3_adapter - command for viewing the adapter logs; for changing the
DEBUG_DATA_FLOW environment variable, modify the stack.yml file

## Services:
- The services are built using the stack.yml file, where all the information needed is stored

### MQTT Broker:
- Mosquitto was used as the MQTT Broker for this project, using the latest image version available
on docker hub.docker.com
- It exposes the 1883 port on localhost - localhost:1833 and uses an initial configuration file for
allowing anonymous clients

### Adapter:
- The adapter was implemented locally and is meant to be "a bridge" between the Mosquitto Broker and
the InfluxDB database - inserting the received MQTT messages on certain topics into the database
- Its environment variables are initialized within the stack.yml file - these are: DEBUG_DATA_FLOW
(used for logging data, only if it is set to True); MOSQUITTO_HOST and INFLUXDB_HOST (the name of
the hosts it will connect to); DB_NAME (the name of the InfluxDB database)
- The json message received for each topic is parsed and inserted into the database in the
following format:
```
	{
            "measurement": station + "." + key,
            "tags": {
                "location": location,
                "station": station
            },
            "time": payload['timestamp'],
            fields": {
                "value": payload[key]
            }
        }
```

### InfluxDB:
- The InfluxDB version 1.8 was used, as it uses InfluxQL instead of Flux (InfluxQL is easier to use,
as it is similar to basic SQL languages)
- The data is stored, for persistence, in a volume

### Grafana:
- The latest image available was used
- It exposes the 80 port on the localhost
- The environment security variables are stored in stack.yml
- The dashboards and datasource are loaded initially (the .yml and .json files), using the locally
stored files; any changes made by the user will be stored within a separate volume locally,for
persistence
- For browser access: localhost:80; authentication: user=asistent, password=grafanaSPRC2023

### MQTT Client:
- The implemented client was created for testing purposes
- It sends a given number of messages, and each is sent every 1 hour (ending with the current time)

### Mentions:
- The stack contains three different networks, that allow the pairs grafana-influxdb,
adapter-mosquitto and adapter-influxdb to communicate independently.

## Resources:
- https://community.grafana.com/t/hide-column-in-table-in-v8-0/49040/7
- https://stackoverflow.com/questions/42731998/how-to-publish-json-data-on-mqtt-broker-in-python
- https://www.influxdata.com/blog/getting-started-python-influxdb/
- https://grafana.com/docs/grafana/latest/administration/provisioning/ 
- https://grafana.com/docs/grafana/latest/datasources/influxdb/query-editor/
- https://stackoverflow.com/questions/54813704/how-to-add-dashboard-configuration-json-file-in-grafana-image 
