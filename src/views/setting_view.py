import flet as ft
from loguru import logger


class Setting_View(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/settings",
            padding=0,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.page = page
        self.controls = [
            ft.AppBar(
                title=ft.Text("Settings"),
                bgcolor=ft.colors.SURFACE_VARIANT,
            ),
            ft.Text("Settings content goes here"),
            ft.ElevatedButton("Go to Main", on_click=self._go_to_main),
        ]
        logger.info("Setting_View initialized.")

    def _go_to_main(self, e):
        self.page.go("/main")
