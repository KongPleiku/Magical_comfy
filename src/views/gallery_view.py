import flet as ft
import os
import base64
from loguru import logger


class Gallery_View(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/gallery",
            padding=0,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            auto_scroll=True,
        )
        self.page = page

        self.temporary_tab = ft.Tab(
            text="Recent",
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src="https://picsum.photos/1080/1920",
                                    width=200,
                                    height=200,
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                margin=10,
                            ),
                        ]
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        self.permanent_tab = ft.Tab(
            text="Gallery",
            content=ft.Column(
                controls=[],
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        self.navigation_tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            expand=True,
            scrollable=True,
            tabs=[self.temporary_tab, self.permanent_tab],
        )

        self.controls = [
            ft.AppBar(
                title=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.IMAGE),
                        ft.Text("Gallery"),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.REFRESH,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        on_click=self._go_to_main,
                    ),
                ],
                bgcolor=ft.Colors.GREY_800,
            ),
            self.navigation_tabs,
        ]
        logger.info("Gallery_View initialized.")

    def _go_to_main(self, e):
        logger.info("Going to main")
        self.page.go("/main")
