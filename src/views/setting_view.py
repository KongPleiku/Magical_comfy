import flet as ft
from loguru import logger
from components.value_slider_containers import Slider_Container_INT


class Setting_View(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/settings",
            padding=0,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            auto_scroll=True,
        )
        self.page = page
        self.controls = [
            ft.AppBar(
                title=ft.Text("Settings"),
                bgcolor=ft.colors.SURFACE_VARIANT,
            ),
            ft.Text("Settings content goes here"),
            ft.ElevatedButton("Go to Main", on_click=self._go_to_main),
            Slider_Container_INT(
                text="Step", min_value=0, max_value=10, divisions=10, initial_value=0
            ),
            Slider_Container_INT(
                text="CFG",
                min_value=0,
                max_value=10,
                divisions=20,
                initial_value=0,
                is_float=True,
            ),
        ]
        logger.info("Setting_View initialized.")

    def _go_to_main(self, e):
        self.page.go("/main")
