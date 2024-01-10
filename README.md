# IOT-Microservices-Platform
## Profeanu Ioana, 343C1 - Tema3 SPRC

## Project run:
- ./run.sh (it is possible to need rights to execute - chmod a+x ./run.sh) - it builds and deploys the services stack
- docker stack rm sprc3 - for removing the stack
- docker swarm init - this command must have been run initially, in order to initialize a docker swarm

## Services:
- The services are built using the stack.yml file, where all the information needed is stored.

### MQTT Broker:
- Mosquitto was used as the MQTT Broker for this project, using the latest image version available on docker hub.docker.com
- It exposes the 1883 port on the localhost and is within the same network as the adaptor - localhost:1833
- It is within the same network as the adapter

### Adapter:
- The adaptor was implemented locally and is meant to be "a bridge" between the Mosquitto Broker and the InfluxDB database.
- Its environment variables are initialized within the stack.yml file - these are: DEBUG_DATA_FLOW (used for logging data, only if it is set to True); MOSQUITTO_HOST and INFLUXDB_HOST (the name of the hosts it will connect to); DB_NAME (the name of the InfluxDB database)
- It is in two networks, in one with InfluxDB and in one with the Mosquitto Broker
- It initially connects to the broker and to the database (it creates the database if it doesn't already exist), and awaits messages from MQTT clients;
- Once a message is received, the topic is parsed and verified (to have the format location/station)
- The payload is parsed:
	- if the timestamp exists, it is formatted to ISO, and if not, it will have the value of the current time
	- each key (if its value is a float or int) in the json is added to an array of datapoints, each datapoint having the following format:
		'''
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
		'''
- The datapoints are inserted in the InfluxDB database

### InfluxDB:
- The InfluxDB version 1.8 was used, as it uses InfluxQL instead of Flux (InfluxQL is easier to use, as it is similar to basic SQL languages)
- The data is stored, for persistance, in a volume
- The service is in two different networks, in one with the adaptor and in one with Grafana

### Grafana:
- The latest image available was used
- It exposes the 80 port on the localhost and is within the same network as the adaptor
- It is within the same network as the adaptor
- The environment security variables are stored in stack.yml
- The dashboards and datasource are loaded initially, using the locally stored files; any changes made by the user will be stored within a separate volume locally, for persistance
- For browser access: localhost:80; authentication: user=asistent, password=grafanaSPRC2023

### MQTT Client:
- The implemented client was created for testing purposes
- It sends a given number of messages, and each is sent every 1 hour (ending with the current time) 

## Resources:
- https://community.grafana.com/t/hide-column-in-table-in-v8-0/49040/7
- https://stackoverflow.com/questions/42731998/how-to-publish-json-data-on-mqtt-broker-in-python
- https://www.influxdata.com/blog/getting-started-python-influxdb/
- https://grafana.com/docs/grafana/latest/administration/provisioning/ 
- https://grafana.com/docs/grafana/latest/datasources/influxdb/query-editor/
- https://stackoverflow.com/questions/54813704/how-to-add-dashboard-configuration-json-file-in-grafana-image 

















- de facut:
- daca primeste timp gresit


https://stackoverflow.com/questions/42731998/how-to-publish-json-data-on-mqtt-broker-in-python

https://www.influxdata.com/blog/getting-started-python-influxdb/

https://stackoverflow.com/questions/54813704/how-to-add-dashboard-configuration-json-file-in-grafana-image 

https://docs.influxdata.com/influxdb/v1/query_language/manage-database/

https://grafana.com/docs/grafana/latest/administration/provisioning/ 
https://grafana.com/docs/grafana/latest/datasources/influxdb/
https://grafana.com/tutorials/provision-dashboards-and-data-sources/
https://grafana.com/docs/grafana/latest/getting-started/get-started-grafana-influxdb/
https://grafana.com/docs/grafana/latest/datasources/influxdb/query-editor/ 

pt tabel 2
https://community.grafana.com/t/hide-column-in-table-in-v8-0/49040/7

https://www.youtube.com/watch?v=cA2mCoIg3ow&t=639s
https://www.youtube.com/watch?v=sGHKY0VmbLw&t=513s
https://www.youtube.com/watch?v=YDzX_nhlG-I

 docker swarm init
docker-compose -f stack.yml build
docker stack deploy -c stack.yml sprc3
 docker stack rm sprc3
/^[^.]+\.[^.]+$/
This query will return all measurements that match the specified pattern. The regular expression ^[^.]+\.[^.]+$ breaks down as follows:

^: Start of the string.
[^.]+: One or more characters that are not a dot.
\.: A literal dot (escaped with a backslash).
[^.]+: One or more characters that are not a dot.
$: End of the string.

~~~~~~~~~~~~~~~~~~~~ de modificat la al doilea dash?
/^[^.]+\.BAT$/


/.*\.BAT$/
.*: Match any sequence of characters (except newline) zero or more times.
\.BAT: Match the literal string ".BAT" at the end of the measurement.
$: Assert the position at the end of the string.

Explanation:

^: Start of the string.
[^.]+: One or more characters that are not a dot.
\.: A literal dot (escaped with a backslash).
[^.]+: One or more characters that are not a dot.
\.: Another literal dot.
BAT: Literal "BAT" at the end.
$: End of the string.


 la url http://influxdb:8086
 la database iot_db

 ioana@ZEPHYRUS:~/SPRC/tema3-mqtt$ docker volume rm sprc3_influxdb_data
sprc3_influxdb_data
ioana@ZEPHYRUS:~/SPRC/tema3-mqtt$ docker volume rm sprc3_grafana_data
sprc3_grafana_data