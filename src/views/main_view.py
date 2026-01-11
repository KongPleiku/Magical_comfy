import flet as ft
from loguru import logger
from components.image_component import Image_component
from components.setting_containers import Setting_container
from components.chat_containers import ChatBar


class Main_View(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/main",
            padding=0,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.page = page
        self.fixed_height = self.page.height

        self.controls = [
            ft.Stack(
                controls=[
                    ft.Container(
                        content=Image_component(),
                        height=self.fixed_height,
                        width=self.page.width,
                    ),
                    Setting_container(),
                    ChatBar(),
                ],
                alignment=ft.alignment.top_center,
                expand=True,
            )
        ]
        logger.info("Main_View initialized.")
