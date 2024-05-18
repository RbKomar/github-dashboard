import requests
from shiny import session


@session.cache
def fetch_repo_data(user, repo):
    url = f'https://api.github.com/repos/{user}/{repo}'
    response = requests.get(url)
    return response.json()


@session.cache
def fetch_user_data(user):
    url = f'https://api.github.com/users/{user}'
    response = requests.get(url)
    return response.json()
