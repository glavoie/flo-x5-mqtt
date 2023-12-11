"""Constants for the flo X5 client."""

# Base URL for API requests.
BASE_URL = "https://account.flo.ca"

# Identity provider information and URLs
ACCOUNT_ID = "6cedc65f-98e2-4651-bdb8-88ee4936c9ba"
CLIENT_ID = "f270e301-24ae-45fb-804d-98b9639f6183"

IDP_BASE_URL = "https://auth.pingone.ca/" + ACCOUNT_ID + "/as"
IDP_AUTHORIZE_URL = IDP_BASE_URL + "/authorize"
IDP_TOKEN_URL = IDP_BASE_URL + "/token"

SCOPE = "eMobility:all"
