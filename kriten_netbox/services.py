import git
import logging
import os
import random
import requests
import string

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

def reach_git_repo(**kwargs):
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    giturl = kwargs.get("giturl")
    branch = kwargs.get("branch")
    token = kwargs.get("token")
    unique_hash = ''.join(random.choices(string.ascii_letters,k=5))
    file_path = f'/tmp/{unique_hash}'
    if token:
        giturl = f'https://{token}@{giturl.split("//")[1]}'
    msg = ""
    try:
        git.Repo.clone_from(giturl,file_path,branch=branch)
    except Exception as e:
        msg = str(e)
        if "not found" in str(e):
            msg = "Repository not found."
        elif "Username" in str(e):
            msg = "Invalid guturl or access token."
        elif "Password" in str(e):
            msg = "Invalid giturl or access token."
        elif "unable to access" in str(e):
            msg = "Invalid access token."
    return msg