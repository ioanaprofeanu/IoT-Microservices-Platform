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
 la database iot_data

 ioana@ZEPHYRUS:~/SPRC/tema3-mqtt$ docker volume rm sprc3_influxdb_data
sprc3_influxdb_data
ioana@ZEPHYRUS:~/SPRC/tema3-mqtt$ docker volume rm sprc3_grafana_data
sprc3_grafana_data