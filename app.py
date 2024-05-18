from shiny import App
from ui.layout import app_ui
from server.handlers import server

app = App(app_ui, server)
