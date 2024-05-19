from shiny import ui


def create_panel_sidebar():
    add_new_account_text = ui.input_text("new_account", "Add GitHub Account", value="RbKomar")
    add_account_button = ui.input_action_button("add_account", "Add Account")
    repo_list = ui.output_ui("repo_list")
    _args = [add_new_account_text, add_account_button, repo_list, ui.hr()]
    return ui.panel_sidebar(*_args, width=3)


def create_main_panel():
    navset_tab = ui.output_ui("dynamic_tabs")
    user_info = ui.column(12, ui.output_ui("user_info")),
    repo_info = ui.column(12, ui.output_ui("repo_info"))
    _args = [navset_tab, user_info, repo_info]
    return ui.panel_main(*_args)


app_ui = ui.page_fluid(ui.panel_title("GitHub Repository Dashboard"),
    ui.layout_sidebar(create_panel_sidebar(), create_main_panel()))
