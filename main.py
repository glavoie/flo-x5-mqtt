"""flo X5 client library."""

import os

from flo_client.auth import Auth

# Main
if __name__ == "__main__":
    # Get username and password from command line
    username = os.environ.get('FLO_USERNAME')
    password = os.environ.get('FLO_PASSWORD')   

    # Create the client
    client = Auth(username, password)

    # Get the token
    token = client.get_access_token()

    # Print the token
    print(token)
