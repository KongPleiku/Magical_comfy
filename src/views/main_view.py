import flet as ft
from loguru import logger
from components.Image_component import Image_component


class Main_View(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/main")
        self.page = page
        self.controls = [Image_component()]
