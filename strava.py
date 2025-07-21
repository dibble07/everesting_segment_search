import logging
import os
import time
from functools import cache

import pandas as pd
import requests  # type: ignore


def update_token():
    """Check and update access token if needed"""

    # check if current token has expired
    if time.time() > float(os.environ.get("expires_at", "0")):

        # request new token
        url = "https://www.strava.com/oauth/token"
        data = {
            "client_id": os.environ["client_id"],
            "client_secret": os.environ["client_secret"],
            "grant_type": "refresh_token",
            "refresh_token": os.environ["refresh_token"],
        }
        response = requests.post(url=url, data=data)

        # store new token and expiry
        if response.status_code == 200:
            response_json = response.json()
            os.environ["access_token"] = response_json["access_token"]
            os.environ["expires_at"] = str(response_json["expires_at"])
            os.environ["refresh_token"] = response_json["refresh_token"]
            logging.info("Token refreshed")
        else:
            logging.warning(
                f"Token refresh failed: {response.status_code} - {response.text}"
            )


@cache
def get_segment_overview(
    lat_lower: float = 51.247,
    lat_upper: float = 51.259,
    long_left: float = -0.325,
    long_right: float = -0.297,
) -> pd.DataFrame:
    """Get cycling climbing segments within bounding box
    :param lat_lower: latitude of lower bound
    :param lat_upper: latitude of upper bound
    :param long_left: longitude of left bound
    :param long_right: longitude of right bound
    """

    # update access token
    update_token()

    # request segments
    url = "https://www.strava.com/api/v3/segments/explore"
    headers = {"Authorization": f"Bearer {os.environ['access_token']}"}
    params = {
        "bounds": f"{lat_lower},{long_left},{lat_upper},{long_right}",
        "activity_type": "riding",
        "min_cat": "1",
    }
    response = requests.get(url, headers=headers, params=params)

    # process segments
    if response.status_code == 200:
        df_overview = pd.DataFrame(response.json()["segments"])
        df_overview.drop(
            columns=[
                "resource_state",
                "climb_category_desc",
                "start_latlng",
                "end_latlng",
                "points",
                "starred",
                "elevation_profile",
                "local_legend_enabled",
            ],
            inplace=True,
        )
        df_overview.set_index("id", inplace=True)
    else:
        logging.warning(f"Error: {response.status_code} - {response.text}")

    return df_overview
