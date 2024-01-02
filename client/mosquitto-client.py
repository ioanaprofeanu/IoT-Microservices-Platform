# import paho.mqtt.client as mqtt
# import json
# from random import choice

# BATS = [99, 18, 117]
# HUMIDS = [40, 200, 19]
# TMPS = [25.3, 27.5, 23.1]
# ALARMS = [0, 13, 2]
# AQIS = [12, 20, 32]
# RSSIS = [1500, 2023, 2051]
# NUM_TOPICS = 100

# def main():
#     client = mqtt.Client()
#     client.connect("localhost")
#     client.loop_start()


#     for _ in range(NUM_TOPICS):
#         payload1 = {
#             "BAT" : choice(BATS),
#             "HUMID" : choice(HUMIDS),
#             "PRJ" : "SPRC",
#             "TMP" : choice(TMPS),
#             "status" : "OK",
#             "timestamp" : "2019−11−26T03 :54:20+03:00"
#         }

#         client.publish('UPB/RPi_1', json.dumps(payload1))

#         payload2 = {
#             "Alarm": choice(ALARMS),
#             "AQI": choice(AQIS),
#             "RSSI": choice(RSSIS)
#         }

#         client.publish('UPB/ZEUS', json.dumps(payload2))

#     client.disconnect()
#     client.loop_stop()

# if __name__ == '__main__':
#     main()

import json
import paho.mqtt.client as mqtt

def on_publish(client, userdata, mid):
    print(f"Message published with MID: {mid}")

def main():
    client = mqtt.Client()

    # set callback for on_publish
    client.on_publish = on_publish

    # Connect to the MQTT broker
    client.connect("localhost", 1883)

    try:
        while True:
            # Take input from the user
            topic = input("Enter the topic: ")

            payload1 = {
                "BAT" : 99,
                "HUMID" : 75,
                "PRJ" : "SPRC",
                "TMP" : 26,
                "status" : "OK",
                # "timestamp" : "2019−11−26T03 :54:20+03:00"
            }

            result = client.publish(topic, json.dumps(payload1))

            # Wait for the message to be published
            result.wait_for_publish()

    except KeyboardInterrupt:
        # Disconnect the client upon keyboard interrupt
        client.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    main()
