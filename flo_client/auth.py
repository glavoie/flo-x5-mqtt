"""Authentification module for the flo X5 API."""

import requests
import logging
import json
import os

from pkce import generate_pkce_pair

from datetime import datetime, timedelta

from flo_client.consts import *


class Auth:
    def __init__(self, username: str, password: str) -> None:
        self.username: str = username
        self.password: str = password
        self.access_token: str | None = None
        self.access_token_expiry: datetime = datetime.now()

        self.logger: logging.Logger = logging.getLogger(__name__)

    def get_access_token(self) -> str:
        if self.access_token is None or self.is_access_token_expired():
            # Check if refresh token is available
            try:
                if os.path.exists("./" + DATA_FOLDER + "/refresh.json"):
                    with open("./" + DATA_FOLDER + "/refresh.json", "r") as f:
                        refresh_token = json.load(f)
                        if "refresh_token" in refresh_token:
                            self.__execute_refresh_flow(refresh_token["refresh_token"])
            except Exception as e:
                self.logger.warn("Error reading refresh token from file: ", e)

        if self.access_token is None or self.is_access_token_expired():
            try:
                self.__execute_full_auth_flow()
            except Exception as e:
                self.logger.warn("Error executing full auth flow: ", e)

        if self.access_token is None:
            raise Exception("Error getting access token.")

        return self.access_token

    def is_access_token_expired(self) -> bool:
        if self.access_token_expiry is None:
            return True
        return self.access_token_expiry < datetime.now()

    def __execute_refresh_flow(self, refresh_token: str) -> None:
        self.logger.info("Refreshing access_token...")

        # Call the token endpoint
        headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "grant_type": "refresh_token",
        }

        resp = requests.post(IDP_TOKEN_URL, headers=headers, data=body)

        if resp.status_code != 200:
            raise Exception(
                "Error calling the token endpoint.", resp.status_code, resp.text
            )

        resp_dict = resp.json()

        self.access_token = resp_dict["access_token"]
        self.access_token_expiry = datetime.now() + timedelta(
            seconds=resp_dict["expires_in"]
        )

        # Save the access_token in json format in a file named refresh.json
        with open("./" + DATA_FOLDER + "/refresh.json", "w") as f:
            refresh_token_file_content = {"refresh_token": resp_dict["refresh_token"]}
            json.dump(refresh_token_file_content, f, indent=4)

    def __execute_full_auth_flow(self) -> None:
        self.logger.info("Executing full authentication flow...")

        # Generate a code_verifier and code_challenge
        code_verifier, code_challenge = generate_pkce_pair()

        # Call the authorize endpoint
        authorize_request_headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        authorize_request_body = {
            "client_id": CLIENT_ID,
            "response_mode": "pi.flow",
            "response_type": "code",
            "scope": "eMobility:all",
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
        }
        resp = requests.post(
            IDP_AUTHORIZE_URL,
            headers=authorize_request_headers,
            data=authorize_request_body,
        )

        if resp.status_code != 200:
            raise Exception(
                "Error calling the IDP_AUTHORIZE_URL endpoint.",
                resp.status_code,
                resp.text,
            )

        resp_dict = resp.json()
        usernamePasswordUrl: str
        if resp_dict["status"] == "USERNAME_PASSWORD_REQUIRED":
            usernamePasswordUrl = resp_dict["_links"]["usernamePassword.check"]["href"]

        # Call the usernamePasswordUrl
        userpass_request_headers = {
            "Accept": "*/*",
            "Content-Type": "application/vnd.pingidentity.usernamePassword.check+json",
        }

        # Post credentials as a json body with the username and password values
        userpass_request_body = {"username": self.username, "password": self.password}

        resp = requests.post(
            usernamePasswordUrl,
            headers=userpass_request_headers,
            json=userpass_request_body,
        )

        if resp.status_code != 200:
            raise Exception(
                "Error calling the usernamePasswordUrl endpoint.",
                resp.status_code,
                resp.text,
            )

        # Save cookies
        cookies = resp.cookies

        resp_dict = resp.json()
        resumeUrl: str
        if resp_dict["status"] == "COMPLETED":
            resumeUrl = resp_dict["resumeUrl"]

        # Call the resumeUrl
        resume_request_headers = {
            "Accept": "*/*",
            "Content-Type": "application/vnd.pingidentity.user.register+json",
        }
        resp = requests.get(resumeUrl, headers=resume_request_headers, cookies=cookies)

        if resp.status_code != 200:
            raise Exception(
                "Error calling the resumeUrl endpoint.", resp.status_code, resp.text
            )

        resp_dict = resp.json()
        code = None
        if resp_dict["status"] == "COMPLETED":
            code = resp.json()["authorizeResponse"]["code"]

        # Call the token endpoint
        token_request_headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        token_request_body = {
            "code": code,
            "code_verifier": code_verifier,
            "client_id": CLIENT_ID,
            "grant_type": "authorization_code",
        }

        resp = requests.post(
            IDP_TOKEN_URL, headers=token_request_headers, data=token_request_body
        )

        if resp.status_code != 200:
            raise Exception(
                "Error calling the token endpoint.", resp.status_code, resp.text
            )

        resp_dict = resp.json()

        self.access_token = resp_dict["access_token"]
        self.access_token_expiry = datetime.now() + timedelta(
            seconds=resp_dict["expires_in"]
        )

        # Save the access_token in json format in a file named refresh.json
        with open("./" + DATA_FOLDER + "/refresh.json", "w") as f:
            refresh_token_file_content = {"refresh_token": resp_dict["refresh_token"]}
            json.dump(refresh_token_file_content, f, indent=4)
