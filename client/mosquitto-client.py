from datetime import datetime, timedelta
import json
import random
import paho.mqtt.client as mqtt

def main():
    client = mqtt.Client()

    client.connect("localhost", 1883)
    client.loop_start()

    iter = int(input("Enter the number of iterations: "))
    # get the current date and time
    initial_date = datetime.now()
    current_date = initial_date

    for i in range(1, iter):
        payload1 = {
            "BAT": random.randint(40, 95),
            "CO": random.uniform(62, 66),
            "PRJ": "SPRC",
            "HUM": random.uniform(35, 37),
            "status": "OK",
            "NO2": random.uniform(0.05, 0.3),
            "O2": random.uniform(10, 13),
            "TC": random.uniform(17, 19),
            "timestamp" : current_date.isoformat()
        }

        result = client.publish('UPB/Gas', json.dumps(payload1))
        result.wait_for_publish()

        current_date = current_date - timedelta(seconds=10)

        payload2 = {
            "BAT": random.randint(70, 100),
            "test": "SPRC112",
            "HUM": random.uniform(34, 38),
            "status": "OK",
            "TC": random.uniform(17, 19),
            "timestamp" : current_date.isoformat()
        }

        result = client.publish('UPB/Mongo', json.dumps(payload2))
        result.wait_for_publish()

        current_date = current_date - timedelta(seconds=10) - timedelta(minutes=20)

        payload3 = {
            "BAT": random.randint(50, 70),
            "test": "SPRC112",
            "HUM": random.uniform(34, 38),
            "timestamp" : current_date.isoformat()
        }

        result = client.publish('UPIT/Cherry', json.dumps(payload3))
        result.wait_for_publish()
        
        current_date = current_date - timedelta(hours=i)

    client.disconnect()
    client.loop_stop()

if __name__ == "__main__":
    main()
