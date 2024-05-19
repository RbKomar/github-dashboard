import logging
from shiny import render, reactive, ui
from shinywidgets import output_widget, render_widget
from server.fetch_data import fetch_repo_data, fetch_user_data, fetch_user_repos
from ui.components import create_clickable_list
from utils.plotting import plot_repo_stats, plot_user_stats, plot_user_repos

def server(input, output, session):
    user = reactive.Value("")
    repo = reactive.Value("")
    accounts = reactive.Value([])
    repositories = reactive.Value({})
    repos_to_show = reactive.Value(5)

    @reactive.Effect
    @reactive.event(input.add_account)
    def _():
        new_account = input.new_account().strip()
        logging.info(f"Adding new account: {new_account}")
        if new_account and new_account not in accounts.get():
            accounts.set(accounts.get() + [new_account])
            repos = fetch_user_repos(new_account)
            logging.info(f"Fetched repos for {new_account}: {repos}")
            repositories.get()[new_account] = repos

    @reactive.Effect
    @reactive.event(input.accounts_nav)
    def _():
        selected_account = input.accounts_nav()
        logging.info(f"Account tab clicked: {selected_account}")
        user.set(selected_account)
        repo.set("")
        repos_to_show.set(5)

    @reactive.Effect
    @reactive.event(input.repo_list_click)
    def _():
        clicked_repo = input.repo_list_click().split('/')
        logging.info(f"Repo clicked: {clicked_repo}")
        if len(clicked_repo) == 2:
            user.set(clicked_repo[0])
            repo.set(clicked_repo[1])

    @reactive.Effect
    @reactive.event(input.see_more_repos)
    def _():
        repos_to_show.set(repos_to_show.get() + 5)

    @output
    @render.ui
    def dynamic_tabs():
        tabs = [ui.nav_panel(account) for account in accounts.get()]
        return ui.navset_tab(*tabs, id="accounts_nav")

    @output
    @render.ui
    def repo_list():
        if user.get() in repositories.get():
            repos = repositories.get()[user.get()]
            if isinstance(repos, list):
                sorted_repos = sorted(repos, key=lambda x: x.get('updated_at', ''), reverse=True)
                displayed_repos = sorted_repos[:repos_to_show.get()]
                see_more_button = ui.input_action_button("see_more_repos", "See More") if len(sorted_repos) > repos_to_show.get() else ui.div()
                return ui.TagList(
                    create_clickable_list([f"{user.get()}/{repo['name']}" for repo in displayed_repos], "repo_list_click"),
                    see_more_button
                )
        return ui.div()

    @output
    @render.ui
    def user_info():
        if user.get():
            data = fetch_user_data(user.get())
            if data:
                return ui.TagList(
                    ui.h3(f"User: {user.get()}"),
                    ui.markdown(f"""
                    **Name:** {data.get('name', 'No name provided')}
                    **Public Repos:** {data.get('public_repos', 0)}
                    **Followers:** {data.get('followers', 0)}
                    **Following:** {data.get('following', 0)}
                    """),
                    output_widget("user_stats"),
                    output_widget("user_repos")
                )
        return ui.div()

    @output
    @render.ui
    def repo_info():
        if user.get() and repo.get():
            data = fetch_repo_data(user.get(), repo.get())
            if data:
                recent_pushes = data.get('recent_pushes', [])
                if isinstance(recent_pushes, list):
                    recent_pushes = "\n".join([
                        f"- {push['commit']['message']} (by {push['commit']['author']['name']} on {push['commit']['author']['date']})"
                        for push in recent_pushes])
                waiting_merges = data.get('waiting_merges', [])
                if isinstance(waiting_merges, list):
                    waiting_merges = "\n".join(
                        [f"- {pull['title']} (created by {pull['user']['login']} on {pull['created_at']})" for pull in waiting_merges]
                    )
                return ui.TagList(
                    ui.h3(f"Repository: {repo.get()}"),
                    ui.markdown(f"""
                    **Description:** {data.get('description', 'No description')}
                    **Stars:** {data.get('stargazers_count', 0)}
                    **Forks:** {data.get('forks_count', 0)}
                    **Open Issues:** {data.get('open_issues_count', 0)}
                    **Recent Pushes:**
                    {recent_pushes}
                    **Waiting Merges:**
                    {waiting_merges}
                    """),
                    output_widget("repo_stats")
                )
        return ui.div()

    @output
    @render_widget
    def user_stats():
        if user.get():
            data = fetch_user_data(user.get())
            if data:
                return plot_user_stats(data)
        return None

    @output
    @render_widget
    def user_repos():
        if user.get():
            repos = fetch_user_repos(user.get())
            if repos:
                return plot_user_repos(repos)
        return None

    @output
    @render_widget
    def repo_stats():
        if user.get() and repo.get():
            data = fetch_repo_data(user.get(), repo.get())
            if data:
                return plot_repo_stats(data)
        return None
