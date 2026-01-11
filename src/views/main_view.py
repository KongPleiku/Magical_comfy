import flet as ft
from loguru import logger
from components.Image_component import Image_component
from components.connection_indicator import ConnectionIndicator


class Main_View(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/main")
        self.page = page
        self.init_view()
        logger.info("Main_View initialized.")

    def init_view(self):
        stack = ft.Stack(
            controls=[
                Image_component(),
                ConnectionIndicator(),
            ]
        )
        self.controls = [stack]
