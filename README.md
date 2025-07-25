# Everesting Segment Search
Application to search for Strava segments in a map area and sort by suitability for everesting

## Setup
1. Clone repository
1. [Create and activate python virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
1. Install [https://pypi.org/project/poetry/] and use it to [install remaining packages](https://python-poetry.org/docs/cli/#install)
1. Create a [Strava API app](https://www.strava.com/settings/api) and set the following environment variables
    - `client_id`
    - `client_secret`
    - `refresh_token`
1. Run the following command to launch the app:
    - `streamlit run app.py`

## Limitations
- The strava API only returns the top 10 items per map area search so zooming in will likely be necessary to get the desired level of detail
- Only segments that are categorised climbs are considered