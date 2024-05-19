from shiny import ui

def create_panel_sidebar():
    _args = [
        ui.input_text("user_name", "GitHub Username", value="RbKomar"),
        ui.input_text("repo_name", "Repository Name", value="github-dashboard"),
        ui.input_action_button("fetch_data", "Fetch Data"),
        ui.hr(),
        ui.input_text("new_account", "Add GitHub Account"),
        ui.input_action_button("add_account", "Add Account"),
        ui.input_text("new_repo", "Add Repository"),
        ui.input_action_button("add_repo", "Add Repository"),
        ui.hr(),
    ]
    return ui.panel_sidebar(*_args, width=3)

def create_main_panel():
    navset_tab = ui.output_ui("dynamic_tabs")
    layout_column = ui.layout_columns(
        ui.column(4, ui.output_ui("repo_list")),
        ui.column(8, ui.output_ui("user_info"), ui.output_ui("repo_info"))
    )
    _args = [navset_tab, layout_column]
    return ui.panel_main(*_args)

app_ui = ui.page_fluid(
    ui.panel_title("GitHub Repository Dashboard"),
    ui.layout_sidebar(create_panel_sidebar(), create_main_panel())
)
