"""flo X5 sync daemon."""

import os
import time
import logging

from flo_client.device import FloX5Device
from flo_client.consts import *

logger = logging.getLogger(__name__)


def configure_logging(log_level):
    level = logging.INFO
    if log_level:
        level = logging.getLevelName(log_level)

    format = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"

    logging.basicConfig(level=level, format=format)


if __name__ == "__main__":
    # Get username and password from command line
    username = os.environ.get("FLO_USERNAME")
    password = os.environ.get("FLO_PASSWORD")
    station_name = os.environ.get("FLO_STATION_NAME")
    log_level = os.environ.get("FLO_LOG_LEVEL")
    hass_mqtt_host = os.environ.get("HASS_MQTT_HOST")
    hass_mqtt_port = os.environ.get("HASS_MQTT_PORT")
    hass_mqtt_username = os.environ.get("HASS_MQTT_USERNAME")
    hass_mqtt_password = os.environ.get("HASS_MQTT_PASSWORD")

    configure_logging(log_level)

    # Check if data folder exists
    if not os.path.exists("./" + DATA_FOLDER):
        raise Exception(
            "Data folder not found: '"
            + DATA_FOLDER
            + "'. Please create it and re-run the application."
        )

    logger.info("Starting flo X5 to MQTT...")
    try:
        # Create the client
        device = FloX5Device(
            username,
            password,
            station_name,
            hass_mqtt_host,
            hass_mqtt_port,
            hass_mqtt_username,
            hass_mqtt_password,
        )

        # Update the status every minute
        while True:
            try:
                device.update_all_sensors()
            except Exception as e:
                logger.error("Error updating sensors: ", e)

            logger.info("Sleeping for " + str(REFRESH_DELAY_SECS) + " seconds...")
            time.sleep(REFRESH_DELAY_SECS)
    except Exception as e:
        logger.error("Error: ", e)
