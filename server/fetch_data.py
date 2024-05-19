import logging
import os

import dotenv
import requests
import requests_cache

# Initialize requests cache
requests_cache.install_cache('github_cache', expire_after=1800)  # Cache for 30 minutes


def get_gh_token():
    dotenv.load_dotenv()
    if GITHUB_TOKEN := os.environ.get('GITHUB_TOKEN'):
        return {"Authorization": f"token {GITHUB_TOKEN}"}
    logging.info("MISSING GH TOKEN")
    return {}


def fetch_repo_data(user, repo):
    headers = get_gh_token()

    url = f'https://api.github.com/repos/{user}/{repo}'
    response = requests.get(url, headers=headers)
    repo_data = response.json()

    url_pushes = f'https://api.github.com/repos/{user}/{repo}/commits'
    response_pushes = requests.get(url_pushes, headers=headers)
    try:
        repo_data['recent_pushes'] = response_pushes.json()[:5]
    except (TypeError, IndexError):
        repo_data['recent_pushes'] = []

    url_pulls = f'https://api.github.com/repos/{user}/{repo}/pulls'
    response_pulls = requests.get(url_pulls, headers=headers)
    try:
        repo_data['waiting_merges'] = response_pulls.json()
    except (TypeError, IndexError):
        repo_data['waiting_merges'] = []

    return repo_data


def fetch_user_data(user):
    headers = get_gh_token()

    url = f'https://api.github.com/users/{user}'
    response = requests.get(url, headers=headers)
    return response.json()


def fetch_user_repos(user):
    headers = get_gh_token()

    url = f'https://api.github.com/users/{user}/repos'
    response = requests.get(url, headers=headers)
    return response.json()
