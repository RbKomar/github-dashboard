from shiny import render, reactive, ui
from server.fetch_data import fetch_repo_data, fetch_user_data, fetch_user_repos
from ui.components import create_info_panel, create_clickable_list
from utils.plotting import plot_repo_stats, plot_user_stats, plot_user_repos
import logging

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

def server(input, output, session):
    user = reactive.Value("")
    repo = reactive.Value("")
    accounts = reactive.Value([])
    repositories = reactive.Value({})

    @reactive.Effect
    @reactive.event(input.fetch_data)
    def _():
        logging.debug(f"Fetching data for user: {input.user_name()}, repo: {input.repo_name()}")
        user.set(input.user_name())
        repo.set(input.repo_name())

    @reactive.Effect
    @reactive.event(input.add_account)
    def _():
        new_account = input.new_account().strip()
        logging.debug(f"Adding new account: {new_account}")
        if new_account and new_account not in accounts.get():
            accounts.set(accounts.get() + [new_account])
            repos = fetch_user_repos(new_account)
            logging.debug(f"Fetched repos for {new_account}: {repos}")
            repositories.get()[new_account] = repos  # Ensure repositories are stored correctly

    @reactive.Effect
    @reactive.event(input.add_repo)
    def _():
        new_repo = input.new_repo().strip()
        logging.debug(f"Adding new repo: {new_repo}")
        if new_repo:
            user_repo = new_repo.split('/')
            if len(user_repo) == 2:
                user_name, repo_name = user_repo
                if user_name not in accounts.get():
                    accounts.set(accounts.get() + [user_name])
                repos = repositories.get().get(user_name, [])
                if not any(repo['name'] == repo_name for repo in repos):
                    repo_data = fetch_repo_data(user_name, repo_name)
                    repos.append(repo_data)
                    repositories.get()[user_name] = repos  # Ensure repositories are stored correctly

    @reactive.Effect
    @reactive.event(input.account_list_click)
    def _():
        clicked_account = input.account_list_click()
        logging.debug(f"Account clicked: {clicked_account}")
        user.set(clicked_account)
        repo.set("")  # Clear the selected repo when account is clicked

    @reactive.Effect
    @reactive.event(input.repo_list_click)
    def _():
        clicked_repo = input.repo_list_click().split('/')
        logging.debug(f"Repo clicked: {clicked_repo}")
        if len(clicked_repo) == 2:
            user.set(clicked_repo[0])
            repo.set(clicked_repo[1])

    @output
    @render.ui
    def dynamic_tabs():
        tabs = [ui.nav_panel(account, ui.h3(f"Repositories for {account}"), ui.output_ui(f"repo_list_{i}")) for i, account in enumerate(accounts.get())]
        return ui.navset_tab(*tabs, id="accounts_nav")

    @output
    @render.ui
    def account_list():
        return create_clickable_list(accounts.get(), "account_list_click")

    @output
    @render.ui
    def repo_list():
        if user.get() in repositories.get():
            repos = repositories.get()[user.get()]
            if isinstance(repos, list):
                # Ensure repos is a list of dictionaries with 'updated_at' keys
                sorted_repos = sorted(repos, key=lambda x: x.get('updated_at', ''), reverse=True)
                return create_clickable_list(
                    [f"{user.get()}/{repo['name']}" for repo in sorted_repos],
                    "repo_list_click"
                )
        return ui.div()

    for i in range(5):
        @output(id=f"repo_list_{i}")
        @render.ui
        def repo_list_content(i=i):
            if i < len(accounts.get()):
                account = accounts.get()[i]
                if account in repositories.get():
                    repos = repositories.get()[account]
                    if isinstance(repos, list):
                        # Ensure repos is a list of dictionaries with 'updated_at' keys
                        sorted_repos = sorted(repos, key=lambda x: x.get('updated_at', ''), reverse=True)
                        return create_clickable_list(
                            [f"{account}/{repo['name']}" for repo in sorted_repos],
                            "repo_list_click"
                        )
            return ui.div()

    @output
    @render.ui
    def user_info():
        data = fetch_user_data(user.get())
        return create_info_panel(
            f"User: {user.get()}",
            f"""
            **Name:** {data.get('name', 'No name provided')}
            **Public Repos:** {data.get('public_repos', 0)}
            **Followers:** {data.get('followers', 0)}
            **Following:** {data.get('following', 0)}
            """
        )

    @output
    @render.ui
    def repo_info():
        data = fetch_repo_data(user.get(), repo.get())
        recent_pushes = data.get('recent_pushes', [])
        if isinstance(recent_pushes, list):
            recent_pushes = "\n".join(
                [f"- {push['commit']['message']} (by {push['commit']['author']['name']} on {push['commit']['author']['date']})" for push in recent_pushes]
            )
        waiting_merges = data.get('waiting_merges', [])
        if isinstance(waiting_merges, list):
            waiting_merges = "\n".join(
                [f"- {pull['title']} (created by {pull['user']['login']} on {pull['created_at']})" for pull in waiting_merges]
            )
        return create_info_panel(
            f"Repository: {repo.get()}",
            f"""
            **Description:** {data.get('description', 'No description')}
            **Stars:** {data.get('stargazers_count', 0)}
            **Forks:** {data.get('forks_count', 0)}
            **Open Issues:** {data.get('open_issues_count', 0)}
            **Recent Pushes:**
            {recent_pushes}
            **Waiting Merges:**
            {waiting_merges}
            """
        )

    @output
    @render.plot
    def user_stats():
        data = fetch_user_data(user.get())
        return plot_user_stats(data)

    @output
    @render.plot
    def user_repos():
        repos = fetch_user_repos(user.get())
        return plot_user_repos(repos)
