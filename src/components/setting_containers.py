# src/components/connection_indicator.py
import flet as ft
from loguru import logger


class Setting_container(ft.Container):
    def __init__(self):
        self.connection_dot = ft.Container(
            width=10,
            height=10,
            shape=ft.BoxShape.CIRCLE,
            bgcolor=ft.colors.RED_500,  # Default to red (not connected)
        )

        self.setting_button = ft.IconButton(
            icon=ft.icons.SETTINGS,
            tooltip="Settings",
            padding=0,
            on_click=lambda e: logger.info("Settings button clicked"),
        )

        self.gallery_button = ft.IconButton(
            icon=ft.icons.IMAGE,
            tooltip="Gallery",
            padding=0,
            on_click=lambda e: logger.info("Gallery button clicked"),
        )

        self.pack = ft.Row(
            controls=[
                self.connection_dot,
                ft.Container(
                    content=ft.Row(
                        controls=[
                            self.setting_button,
                            self.gallery_button,
                        ],
                        spacing=0,
                    ),
                    bgcolor=ft.colors.WHITE,
                    border_radius=90,
                ),
            ],
            adaptive=True,
            spacing=10,
        )

        super().__init__(
            top=30,
            right=5,
            content=self.pack,
        )
