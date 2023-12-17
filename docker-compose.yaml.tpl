version: "3"
services:
  flo-x5-mqtt:
    image: flo-x5-mqtt
    restart: always
    environment:
      HASS_MQTT_USERNAME: ''
      HASS_MQTT_PASSWORD: ''
      HASS_MQTT_HOST: '192.168.1.NN'
      HASS_MQTT_PORT: '1883'
      FLO_USERNAME: ''
      FLO_PASSWORD: ''
      FLO_STATION_NAME: 'AAE-NNNNN'
    volumes:
      - ./data:/app/data
