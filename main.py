"""flo X5 client library."""

import os
import time
from datetime import datetime

from flo_client.client import FloX5Client

from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo, Sensor, SensorInfo

from flo_client.consts import *

session_id = None

# Main
def update_station_online_sensor(client, station, mqtt_settings, device_info):
    online_sensor_info = BinarySensorInfo(name="Station Online", device_class="connectivity", unique_id="status", device=device_info)
    online_sensor_settings = Settings(mqtt=mqtt_settings, entity=online_sensor_info)

        # Instantiate the sensor
    online_sensor = BinarySensor(online_sensor_settings)

        # Change the state of the sensor, publishing an MQTT message that gets picked up by HA
    if client.is_station_online(station):
        online_sensor.on()
    else:
        online_sensor.off()

def update_vehicle_connected_sensor(client, station, mqtt_settings, device_info):
    vehicle_connected_sensor_info = BinarySensorInfo(name="Vehicle Connected", device_class="connectivity", unique_id="vehicle_connected", device=device_info)
    vehicle_connected_sensor_settings = Settings(mqtt=mqtt_settings, entity=vehicle_connected_sensor_info)

        # Instantiate the sensor
    vehicle_connected_sensor = BinarySensor(vehicle_connected_sensor_settings)

        # Change the state of the sensor, publishing an MQTT message that gets picked up by HA
    if client.is_vehicle_connected(station):
        vehicle_connected_sensor.on()
    else:
        vehicle_connected_sensor.off()

def update_vehicle_charging_sensor(client, station, session, mqtt_settings, device_info):
    # Charging sensor
    vehicle_charging_sensor_info = BinarySensorInfo(name="Vehicle Charging", 
                                                    device_class="battery_charging", 
                                                    unique_id="vehicle_charging", 
                                                    device=device_info)
    vehicle_charging_sensor_settings = Settings(mqtt=mqtt_settings, entity=vehicle_charging_sensor_info)
    vehicle_charging_sensor = BinarySensor(vehicle_charging_sensor_settings)

    # Amperage sensor
    amperage_charging_sensor_info = SensorInfo(name="Amperage", 
                                               unit_of_measurement="A", 
                                               state_class="measurement", 
                                               device_class="current", 
                                               unique_id="amperage_charging", 
                                               device=device_info)
    amperage_charging_sensor_settings = Settings(mqtt=mqtt_settings, entity=amperage_charging_sensor_info)
    amperage_charging_sensor = Sensor(amperage_charging_sensor_settings)

    # Amperage offered sensor
    amperage_offered_sensor_info = SensorInfo(name="Amperage Offered", 
                                              unit_of_measurement="A", 
                                              state_class="measurement", 
                                              device_class="current", 
                                              unique_id="amperage_offered", 
                                              device=device_info)
    amperage_offered_sensor_settings = Settings(mqtt=mqtt_settings, entity=amperage_offered_sensor_info)
    amperage_offered_sensor = Sensor(amperage_offered_sensor_settings)
    
    # Voltage sensor
    voltage_sensor_info = SensorInfo(name="Voltage", 
                                     unit_of_measurement="V", 
                                     state_class="measurement", 
                                     device_class="voltage", 
                                     unique_id="voltage", 
                                     device=device_info)
    voltage_sensor_settings = Settings(mqtt=mqtt_settings, entity=voltage_sensor_info)
    voltage_sensor = Sensor(voltage_sensor_settings)

    # Energy transferred sensor 
    energy_transferred_sensor_info = SensorInfo(name="Energy Transferred", 
                                                unit_of_measurement="kWh", 
                                                state_class="total_increasing", 
                                                device_class="energy", 
                                                unique_id="session_energy_transferred", 
                                                device=device_info)
    energy_transferred_sensor_settings = Settings(mqtt=mqtt_settings, entity=energy_transferred_sensor_info)
    energy_transferred_sensor = Sensor(energy_transferred_sensor_settings)

    # Change the state of the sensor, publishing an MQTT message that gets picked up by HA
    if client.is_vehicle_charging(station):
        vehicle_charging_sensor.on()

        if session is not None:
            if session[SESSION_ID] != get_last_session_id():
                # New session, reset the energy transferred sensor to avoid duplicate total energy computation.
                energy_transferred_sensor.set_state(0)
                save_last_session_id(session[SESSION_ID])

            amperage_charging_sensor.set_state(float(session[SESSION_AMPERAGE]))
            amperage_offered_sensor.set_state(float(session[SESSION_AMPERAGE_OFFERED]))
            voltage_sensor.set_state(float(session[SESSION_VOLTAGE]))

            # Convert from Wh to kWh with 2 decimal points.
            energy_transferred_sensor.set_state("{:.2f}".format(float(session[SESSION_ENERGY_TRANSFERRED_WH]) / 1000))
    else:
        vehicle_charging_sensor.off()
        amperage_charging_sensor.set_state(0)
        amperage_offered_sensor.set_state(0)
        voltage_sensor.set_state(0)


def save_last_session_id(session_id: str):
    with open("./data/last-session", "w") as f:
        f.write(session_id)

def get_last_session_id():
    if os.path.exists("./data/last-session"):
        with open("./data/last-session", "r") as f:
            return f.read()
    return None

if __name__ == "__main__":
    # Get username and password from command line
    username = os.environ.get('FLO_USERNAME')
    password = os.environ.get('FLO_PASSWORD')   
    station_name = os.environ.get('FLO_STATION_NAME')
    hass_mqtt_host = os.environ.get('HASS_MQTT_HOST')
    hass_mqtt_port = os.environ.get('HASS_MQTT_PORT')
    hass_mqtt_username = os.environ.get('HASS_MQTT_USERNAME')
    hass_mqtt_password = os.environ.get('HASS_MQTT_PASSWORD')

    print("Starting sync...")

    # Create the client
    client = FloX5Client(username, password)

    while True:
        # Get the token
        station = client.get_station_by_name(station_name)

        station_id = station["information"]["id"]
        session = client.get_session_by_id(station_id)

        # Configure the required parameters for the MQTT broker
        mqtt_settings = Settings.MQTT(host=hass_mqtt_host, port=hass_mqtt_port, username=hass_mqtt_username, password=hass_mqtt_password)

        # Define the device. At least one of `identifiers` or `connections` must be supplied
        device_info = DeviceInfo(name="Flo X5: " + station["information"]["name"], 
                                 model=station["information"]["model"],
                                 manufacturer="AddEnergie",
                                 identifiers=station_id
                                 )

        update_station_online_sensor(client, station, mqtt_settings, device_info)
        update_vehicle_connected_sensor(client, station, mqtt_settings, device_info)
        update_vehicle_charging_sensor(client, station, session, mqtt_settings, device_info)

        print("Sleeping for 60 seconds...")
        time.sleep(60)
