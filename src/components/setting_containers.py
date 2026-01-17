# src/components/connection_indicator.py
import flet as ft
from loguru import logger
from route import navigator

from services.client_services import client
from utils.event_bus import event_bus


class Setting_container(ft.Container):
    def __init__(self):
        self.connection_dot = ft.Container(
            width=10,
            height=10,
            shape=ft.BoxShape.CIRCLE,
            bgcolor=ft.Colors.RED_500,  # Default to red (not connected)
        )

        self.setting_button = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            tooltip="Settings",
            padding=0,
            on_click=self._on_setting_click,
        )

        self.gallery_button = ft.IconButton(
            icon=ft.Icons.IMAGE,
            tooltip="Gallery",
            padding=0,
            on_click=self._on_gallery_click,
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
                    bgcolor=ft.Colors.WHITE,
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

        self._init_connection_dot()
        event_bus.subscribe("connected", self._on_connected)
        event_bus.subscribe("disconnected", self._on_disconnected)

    def _init_connection_dot(self):
        if client.connected:
            self.connection_dot.bgcolor = ft.Colors.GREEN_500

        else:
            self.connection_dot.bgcolor = ft.Colors.RED_500

    def _on_connected(self):
        self.connection_dot.bgcolor = ft.Colors.GREEN

    def _on_disconnected(self):
        self.connection_dot.bgcolor = ft.Colors.RED

    def _on_setting_click(self, e):
        logger.info("Setting button clicked")
        navigator.go_to_settings()

    def _on_gallery_click(self, e):
        logger.info("Gallery button clicked")
        navigator.go_to_gallery()
