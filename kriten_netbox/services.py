import json
import logging
import requests

def reach_cluster(**kwargs):
    logger = logging.getLogger('netbox.views.ObjectEditView')
    kriten_url = kwargs.get("kriten_url")
    api_token = kwargs.get("api_token")
    headers = {
        "Content-Type": "application/json",
        "Token": api_token
    }
    runners_url = f"{kriten_url}/api/v1/runners"
    try:
        list_runners = requests.get(runners_url, headers=headers)
        if list_runners.status_code != 200:
            logger.warning(f"Failed to list runners: {kriten_url}.")
            return False
    except Exception as e:
        logger.warning(f"Failed to connect: {str(e)}.")
        return False
    return True
