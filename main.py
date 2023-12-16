"""flo X5 client library."""

import os
import time

from flo_client.client import FloX5Client

from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo

# Main
if __name__ == "__main__":
    # Get username and password from command line
    username = os.environ.get('FLO_USERNAME')
    password = os.environ.get('FLO_PASSWORD')   
    hass_mqtt_host = os.environ.get('HASS_MQTT_HOST')
    hass_mqtt_port = os.environ.get('HASS_MQTT_PORT')
    hass_mqtt_username = os.environ.get('HASS_MQTT_USERNAME')
    hass_mqtt_password = os.environ.get('HASS_MQTT_PASSWORD')

    # Create the client
    client = FloX5Client(username, password)


    while True:
        # Get the token
        station = client.get_station_by_name("AAE-00689")

        # Pretty print the station
        # print("### Station: AAE-00689 ###")
        # print(json.dumps(station, indent=4, sort_keys=True))

        station_id = station["information"]["id"]
        session = client.get_session_by_id(station_id)

        #Pretty print the session
        # print("### Session ###")
        # print(json.dumps(session, indent=4, sort_keys=True))

        # Configure the required parameters for the MQTT broker
        mqtt_settings = Settings.MQTT(host=hass_mqtt_host, port=hass_mqtt_port, username=hass_mqtt_username, password=hass_mqtt_password)

        # Define the device. At least one of `identifiers` or `connections` must be supplied
        device_info = DeviceInfo(name="Flo X5: " + station["information"]["name"], 
                                 model=station["information"]["model"],
                                 manufacturer="AddEnergie",
                                 identifiers=station_id
                                 )

        online_sensor_info = BinarySensorInfo(name="Station Online", device_class="connectivity", unique_id="status", device=device_info)
        online_sensor_settings = Settings(mqtt=mqtt_settings, entity=online_sensor_info)

        # Instantiate the sensor
        online_sensor = BinarySensor(online_sensor_settings)

        # Change the state of the sensor, publishing an MQTT message that gets picked up by HA
        if station["status"]["state"] == "Available":
            online_sensor.on()
        else:
            online_sensor.off()

        charging_sensor_info = BinarySensorInfo(name="Vehicle Charging", device_class="power", unique_id="charging", device=device_info)
        charging_sensor_settings = Settings(mqtt=mqtt_settings, entity=charging_sensor_info)

        # Instantiate the sensor
        charging_sensor = BinarySensor(charging_sensor_settings)

        # Change the state of the sensor, publishing an MQTT message that gets picked up by HA
        if session is not None:
            charging_sensor.on()
        else:
            charging_sensor.off()

        print("Sleeping for 60 seconds...")
        time.sleep(60)