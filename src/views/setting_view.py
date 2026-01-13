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

        self.generation_paramters_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Paramters", size=18, weight="bold"),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            ft.TextField(
                                label="Width",
                                expand=True,
                                value="512",
                                border_radius=20,
                            ),
                            ft.IconButton(icon=ft.icons.FLIP),
                            ft.TextField(
                                label="Height",
                                expand=True,
                                value="512",
                                border_radius=20,
                            ),
                        ]
                    ),
                    Slider_Container_INT(
                        text="Steps",
                        min_value=1,
                        max_value=30,
                        divisions=30,
                        initial_value=20,
                    ),
                    Slider_Container_INT(
                        text="CFG",
                        min_value=1,
                        max_value=10,
                        divisions=18,
                        initial_value=5,
                        is_float=True,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Dropdown(
                                label="Sampler",
                                border_radius=20,
                                value="euler_ancestral",
                                options=[
                                    ft.dropdown.Option("euler_ancestral"),
                                ],
                                expand=True,
                            ),
                            ft.Dropdown(
                                label="Scheduler",
                                border_radius=20,
                                value="sgm_uniform",
                                options=[
                                    ft.dropdown.Option("sgm_uniform"),
                                ],
                                expand=True,
                            ),
                        ],
                    ),
                    ft.Text("Seed", size=18, weight="bold"),
                    ft.Divider(),
                ],
                spacing=5,
            ),
            padding=10,
            margin=10,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=20,
        )

        self.face_detailer_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Switch(
                        label="Face Detailer",
                        value=False,
                    ),
                    ft.Column(
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Dropdown(
                                        label="Sampler",
                                        border_radius=20,
                                        value="euler_ancestral",
                                        options=[
                                            ft.dropdown.Option("euler_ancestral"),
                                        ],
                                        expand=True,
                                    ),
                                    ft.Dropdown(
                                        label="Scheduler",
                                        border_radius=20,
                                        value="sgm_uniform",
                                        options=[
                                            ft.dropdown.Option("sgm_uniform"),
                                        ],
                                        expand=True,
                                    ),
                                ],
                            ),
                            Slider_Container_INT(
                                text="Steps",
                                min_value=1,
                                max_value=30,
                                divisions=30,
                                initial_value=20,
                            ),
                            Slider_Container_INT(
                                text="CFG",
                                min_value=1,
                                max_value=10,
                                divisions=18,
                                initial_value=5,
                                is_float=True,
                            ),
                        ]
                    ),
                ]
            ),
            padding=10,
            margin=10,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=20,
        )

        self.Tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            expand=True,
            scrollable=True,
            tabs=[
                ft.Tab(
                    text="Generation",
                    content=ft.Column(
                        controls=[
                            self.generation_paramters_container,
                            self.face_detailer_container,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ),
            ],
        )
        self.controls = [
            ft.AppBar(
                title=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SETTINGS),
                        ft.Text("Settings"),
                    ],
                    spacing=10,  # Adjust this to change the gap between the icon and text
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Ensures they align vertically
                ),
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        on_click=self._go_to_main,
                    )
                ],
                bgcolor=ft.colors.SURFACE_VARIANT,
            ),
            self.Tabs,
        ]
        logger.info("Setting_View initialized.")

    def _go_to_main(self, e):
        self.page.go("/main")
