# flo-x5-mqtt
Daemon to synchronize the state information of flo X5 EV chargers from the flo.ca API to HomeAssistant using MQTT.

## Pre-requisites
### Install Dependencies
To install dependencies:
`pip install requests ha_mqtt_discoverable pkce`

### Configure Environment Variables
The configuration is done through environment variables:

| Variable                | Description                                           |
|-------------------------|-------------------------------------------------------|
| `FLO_USERNAME`          | Username of the flo.ca account.                       |
| `FLO_PASSWORD`          | Password of the flo.ca account.                       |
| `FLO_STATION_NAME`      | Name of the flo X5 charging station (ex: AAE-00123).  |
| `FLO_LOG_LEVEL`         | Log level. Default: INFO                              |
| `HASS_MQTT_HOST`        | Host/IP of the MQTT server.                           |
| `HASS_MQTT_PORT`        | Port of the MQTT server.                              |
| `HASS_MQTT_USERNAME`    | Username for the MQTT server.                         |
| `HASS_MQTT_PASSWORD`    | Password for the MQTT server.                         |

### Create the `data` folder
The application uses a folder called `data` to store some state information. Create it next to `main.py` before running the application.

## Run the application
`python main.py`

## Run using Docker Compose
To use with Docker Compose, create your `docker-compose.yaml` file with the following content:
```
version: "3"
services:
  AAE-00123:
    image: glavoie84/flo-x5-mqtt:latest
    restart: unless-stopped
    environment:
      HASS_MQTT_USERNAME: ''
      HASS_MQTT_PASSWORD: ''
      HASS_MQTT_HOST: '<host or IP>'
      HASS_MQTT_PORT: '1883'
      FLO_USERNAME: ''
      FLO_PASSWORD: ''
      FLO_STATION_NAME: 'AAE-00123'
    volumes:
      - ./data:/app/data
```

## Building the Docker Image
`docker build -t flo-x5-mqtt .`