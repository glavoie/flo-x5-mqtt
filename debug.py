"""flo X5 API dump."""

import os
import json

from flo_client.client import FloX5Client

# Main
if __name__ == "__main__":
    # Get username and password from command line
    username = os.environ.get("FLO_USERNAME")
    password = os.environ.get("FLO_PASSWORD")
    station_name = os.environ.get("FLO_STATION_NAME")
    hass_mqtt_host = os.environ.get("HASS_MQTT_HOST")
    hass_mqtt_port = os.environ.get("HASS_MQTT_PORT")
    hass_mqtt_username = os.environ.get("HASS_MQTT_USERNAME")
    hass_mqtt_password = os.environ.get("HASS_MQTT_PASSWORD")

    # Create the client
    client = FloX5Client(username, password)

    # Get the token
    station = client.get_station_by_name(station_name)

    # Pretty print the station
    print("### Station: " + station_name + " ###")
    print(json.dumps(station, indent=4, sort_keys=True))

    station_id = station["information"]["id"]
    session = client.get_session_by_id(station_id)

    print("")

    # Pretty print the session
    print("### Session ###")
    print(json.dumps(session, indent=4, sort_keys=True))
