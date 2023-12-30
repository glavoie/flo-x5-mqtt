"""Constants for the flo X5 client."""

# Base constants
REFRESH_DELAY_SECS = 60
DATA_FOLDER = "data"

# Base URL for API requests.
BASE_URL = "https://emobility.flo.ca"
STATIONS_URL = BASE_URL + "/v3.0/user/stations"
SESSIONS_URL = BASE_URL + "/v3.0/user/sessions"

# Identity provider information and URLs
ACCOUNT_ID = "6cedc65f-98e2-4651-bdb8-88ee4936c9ba"
CLIENT_ID = "f270e301-24ae-45fb-804d-98b9639f6183"

IDP_BASE_URL = "https://auth.pingone.ca/" + ACCOUNT_ID + "/as"
IDP_AUTHORIZE_URL = IDP_BASE_URL + "/authorize"
IDP_TOKEN_URL = IDP_BASE_URL + "/token"

SCOPE = "eMobility:all"

REFRESH_DELAY_SECS = 60

# Status constants
STATUS_KEY = "status"

# Charging station state
STATE_KEY = "state"
STATE_AVAILABLE = "Available"
STATE_INUSE = "InUse"

# Vehicle state
PILOT_STATE_KEY = "pilotSignalState"
PILOT_STATE_DISCONNECTED = "A"
PILOT_STATE_CONNECTED = "B"
PILOT_STATE_CHARGING = "C"

# Session state
SESSION_NOT_CHARGING = "NotCharging"
SESSION_CHARGING = "Charging"
SESSION_COMPLETED = "Completed"

# Session constants
SESSION_ID = "id"
SESSION_AMPERAGE = "amperage"
SESSION_AMPERAGE_OFFERED = "amperageOffer"
SESSION_VOLTAGE = "voltage"
SESSION_ENERGY_TRANSFERRED_WH = "energyTransferredWh"
SESSION_DURATION_MS = "durationMs"
SESSION_START_DATE = "startDate"
