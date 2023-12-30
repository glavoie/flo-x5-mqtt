"""Client for the flo X5 API."""

import logging
import json
import requests

from datetime import datetime, timedelta
from flo_client.auth import Auth
from flo_client.consts import *


class FloX5Client:
    def __init__(self, username: str, password: str) -> None:
        self.next_refresh = datetime.now()
        self._auth = Auth(username, password)

        self._refresh()

    def _refresh(self) -> None:
        # Refresh every minutes at most
        if datetime.now() < self.next_refresh:
            return

        self._stations = self._get_stations()
        self._sessions = self._get_sessions()

        self.next_refresh = datetime.now() + timedelta(seconds=REFRESH_DELAY_SECS)

    def _get_stations(self) -> dict:
        resp = requests.get(STATIONS_URL, headers=self._get_headers())
        if resp.status_code != 200:
            raise Exception("Error getting stations.", resp.status_code, resp.text)

        # Convert the result to a list of Station objects
        stations = json.loads(resp.text)

        return resp.json()

    def _get_sessions(self) -> dict:
        resp = requests.get(SESSIONS_URL, headers=self._get_headers())
        if resp.status_code != 200:
            raise Exception("Error getting sessions.", resp.status_code, resp.text)
        return resp.json()

    def _get_headers(self) -> dict:
        return {
            "Accept": "*/*",
            "Authorization": "Bearer " + self._auth.get_access_token(),
        }

    def get_station_by_name(self, name: str) -> dict | None:
        self._refresh()
        for station in self._stations:
            if station["information"]["name"] == name:
                return station

        return None

    def get_session_by_id(self, id: str) -> dict | None:
        self._refresh()
        for session in self._sessions:
            if session["station"]["id"] == id:
                return session

        return None

    def is_station_online(self, station: dict | None) -> bool:
        if station is None:
            return False

        return (
            station[STATUS_KEY][STATE_KEY] == STATE_AVAILABLE
            or station[STATUS_KEY][STATE_KEY] == STATE_INUSE
        )

    def is_vehicle_connected(self, station: dict | None) -> bool:
        if station is None:
            return False

        return (
            station[STATUS_KEY][PILOT_STATE_KEY] == PILOT_STATE_CONNECTED
            or station[STATUS_KEY][PILOT_STATE_KEY] == PILOT_STATE_CHARGING
        )

    def is_vehicle_charging(self, station: dict | None) -> bool:
        if station is None:
            return False

        return station[STATUS_KEY][PILOT_STATE_KEY] == PILOT_STATE_CHARGING
