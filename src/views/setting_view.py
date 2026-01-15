import flet as ft
from loguru import logger
from components.value_slider_containers import Slider_Container_INT
from services.setting_services import settings_services
from services.client_services import client
import random
import asyncio


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
        self.random_seed = settings_services.settings.generation.random_seed

        # WIDTH FIELD
        self.width_text_field = ft.TextField(
            label="Width",
            expand=True,
            value=settings_services.settings.generation.width,
            border_radius=20,
            on_change=lambda e: (
                settings_services.set_generation_value("width", int(e.control.value)),
            ),
        )

        # HEIHGT_FIELD
        self.height_text_field = ft.TextField(
            label="Height",
            expand=True,
            value=settings_services.settings.generation.height,
            border_radius=20,
            on_change=lambda e: (
                settings_services.set_generation_value("height", int(e.control.value)),
            ),
        )

        # SWAP BUTTON
        self.swap_heigth_and_width_button = ft.IconButton(
            icon=ft.Icons.SWAP_HORIZ, on_click=self._on_swap_button_clicked
        )

        # SEED_FIELD
        self.seed_field = ft.TextField(
            label="Seed",
            expand=True,
            value=settings_services.settings.generation.last_seed,
            border_radius=20,
            on_change=lambda e: (
                settings_services.set_generation_value(
                    "last_seed", int(e.control.value)
                )
            ),
        )

        self.random_seed_button = ft.IconButton(
            icon=ft.Icons.CASINO, on_click=self._on_random_seed_clicked
        )

        self.lock_seed_button = ft.IconButton(
            icon=ft.Icons.LOCK, on_click=self._on_lock_seed_clicked
        )

        self.save_image_after_generation_switch = ft.Switch(
            label="Save image after generation",
            value=settings_services.settings.generation.save_on_generate,
            on_change=self._on_save_image_after_generation_switch,
        )

        self.generation_paramters_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Paramters", size=18, weight="bold"),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            self.width_text_field,
                            self.swap_heigth_and_width_button,
                            self.height_text_field,
                        ]
                    ),
                    Slider_Container_INT(
                        text="Steps",
                        min_value=1,
                        max_value=30,
                        divisions=29,
                        initial_value=settings_services.settings.generation.steps,
                        on_change=lambda e: (
                            settings_services.set_generation_value(
                                "steps", int(e.control.value)
                            )
                        ),
                    ),
                    Slider_Container_INT(
                        text="CFG",
                        min_value=1,
                        max_value=10,
                        divisions=18,
                        initial_value=settings_services.settings.generation.cfg,
                        is_float=True,
                        on_change=lambda e: (
                            settings_services.set_generation_value(
                                "cfg", e.control.value
                            )
                        ),
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Dropdown(
                                label="Sampler",
                                border_radius=20,
                                value=settings_services.settings.generation.sampler_name,
                                options=[
                                    ft.dropdown.Option("euler_ancestral"),
                                ],
                                expand=True,
                                on_change=lambda e: (
                                    settings_services.set_generation_value(
                                        "sampler_name", e.control.value
                                    )
                                ),
                            ),
                            ft.Dropdown(
                                label="Scheduler",
                                border_radius=20,
                                value=settings_services.settings.generation.scheduler,
                                options=[
                                    ft.dropdown.Option("sgm_uniform"),
                                ],
                                expand=True,
                                on_change=lambda e: (
                                    settings_services.set_generation_value(
                                        "scheduler", e.control.value
                                    )
                                ),
                            ),
                        ],
                    ),
                    ft.Text("Seed", size=18, weight="bold"),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            self.seed_field,
                            self.random_seed_button,
                            self.lock_seed_button,
                        ]
                    ),
                    self.save_image_after_generation_switch,
                ],
                spacing=5,
            ),
            padding=10,
            margin=10,
            bgcolor=ft.Colors.GREY_800,
            border_radius=20,
        )

        self.face_detailer_switch = ft.Switch(
            label="Face Detailer",
            value=settings_services.settings.generation.use_face_detailer,
            on_change=self._on_face_detailer_switch,
        )

        self.face_detailer_settings_column = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Dropdown(
                            label="Sampler",
                            border_radius=20,
                            value=settings_services.settings.face_detailer.sampler_name,
                            options=[
                                ft.dropdown.Option("euler_ancestral"),
                            ],
                            expand=True,
                            on_change=lambda e: (
                                settings_services.set_face_detailer_value(
                                    "sampler_name", e.control.value
                                )
                            ),
                        ),
                        ft.Dropdown(
                            label="Scheduler",
                            border_radius=20,
                            value=settings_services.settings.face_detailer.scheduler,
                            options=[
                                ft.dropdown.Option("sgm_uniform"),
                            ],
                            expand=True,
                            on_change=lambda e: (
                                settings_services.set_face_detailer_value(
                                    "scheduler", e.control.value
                                )
                            ),
                        ),
                    ],
                ),
                Slider_Container_INT(
                    text="Steps",
                    min_value=1,
                    max_value=30,
                    divisions=29,
                    initial_value=settings_services.settings.face_detailer.steps,
                    on_change=lambda e: (
                        settings_services.set_face_detailer_value(
                            "steps", int(e.control.value)
                        )
                    ),
                ),
                Slider_Container_INT(
                    text="CFG",
                    min_value=1,
                    max_value=10,
                    divisions=18,
                    initial_value=settings_services.settings.face_detailer.cfg,
                    is_float=True,
                    on_change=lambda e: (
                        settings_services.set_face_detailer_value(
                            "cfg", e.control.value
                        )
                    ),
                ),
                Slider_Container_INT(
                    text="Denoising Strength",
                    min_value=0,
                    max_value=1,
                    divisions=20,
                    initial_value=settings_services.settings.face_detailer.denoise,
                    is_float=True,
                    on_change=lambda e: (
                        settings_services.set_face_detailer_value(
                            "denoise", e.control.value
                        )
                    ),
                ),
                Slider_Container_INT(
                    text="Face detection threshold",
                    min_value=0,
                    max_value=1,
                    divisions=20,
                    initial_value=settings_services.settings.face_detailer.bbox_threshold,
                    is_float=True,
                    on_change=lambda e: (
                        settings_services.set_face_detailer_value(
                            "bbox_threshold", e.control.value
                        )
                    ),
                ),
                Slider_Container_INT(
                    text="Face detection crop factor",
                    min_value=1,
                    max_value=4,
                    divisions=6,
                    initial_value=settings_services.settings.face_detailer.bbox_crop_factor,
                    is_float=True,
                    on_change=lambda e: (
                        settings_services.set_face_detailer_value(
                            "bbox_crop_factor", e.control.value
                        )
                    ),
                ),
            ]
        )

        self.Host_section = ft.TextField(
            label="Host",
            expand=True,
            value=settings_services.settings.connection.host,
            border_radius=20,
            on_change=lambda e: (
                settings_services.set_connection_value("host", e.control.value)
            ),
        )

        self.Port_section = ft.TextField(
            label="Port",
            expand=True,
            value=settings_services.settings.connection.port,
            border_radius=20,
            on_change=lambda e: (
                settings_services.set_connection_value("port", e.control.value)
            ),
        )

        self.Connect_button = ft.Button(
            text="Connect",
            on_click=self._on_connect_button_clicked,
            bgcolor=ft.Colors.GREY_800,
        )

        self.Connection_string = ft.Text(
            value="Disconnected", size=18, weight="bold", color=ft.Colors.RED
        )

        self.connection_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Connection", size=18, weight="bold"),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            self.Host_section,
                            self.Port_section,
                        ]
                    ),
                    self.Connect_button,
                    self.Connection_string,
                ]
            ),
            padding=10,
            margin=10,
            bgcolor=ft.Colors.GREY_800,
            border_radius=20,
        )

        self.face_detailer_container = ft.Container(
            content=ft.Column(
                controls=[self.face_detailer_switch, self.face_detailer_settings_column]
            ),
            padding=10,
            margin=10,
            bgcolor=ft.Colors.GREY_800,
            border_radius=20,
        )

        self.generation_settings_tab = ft.Tab(
            text="Generation",
            content=ft.Column(
                controls=[
                    self.generation_paramters_container,
                    self.face_detailer_container,
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        self.connection_settings_tab = ft.Tab(
            text="Connection", content=self.connection_container
        )

        self.Tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            expand=True,
            scrollable=True,
            tabs=[self.generation_settings_tab, self.connection_settings_tab],
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
                bgcolor=ft.Colors.GREY_800,
            ),
            self.Tabs,
        ]

        self._init_lock_seed()
        self._init_face_detailer_setting_column()
        self._init_connection_settings()

        logger.info("Setting_View initialized.")

    # INITAL FUNCTION
    def _init_lock_seed(self):
        if not self.random_seed:
            self.lock_seed_button.icon = ft.Icons.LOCK
            self.seed_field.disabled = False

        else:
            self.lock_seed_button.icon = ft.Icons.LOCK_OPEN
            self.seed_field.disabled = True
        self.page.update()

    def _init_face_detailer_setting_column(self):
        if not self.face_detailer_switch.value:
            self.face_detailer_settings_column.visible = False
            settings_services.set_generation_value("use_face_detailer", False)

        else:
            self.face_detailer_settings_column.visible = True
            settings_services.set_generation_value("use_face_detailer", True)

        self.page.update()

    def _init_connection_settings(self):
        self.Host_section.value = settings_services.settings.connection.host
        self.Port_section.value = settings_services.settings.connection.port

        if client.connected:
            self.Connection_string.value = "Connected"
            self.Connection_string.color = ft.Colors.GREEN

        else:
            self.Connection_string.value = "Disconnected"
            self.Connection_string.color = ft.Colors.RED

        self.page.update()

    # INTERACTION FUNCTION
    def _on_lock_seed_clicked(self, e):
        if not self.random_seed:
            self.random_seed = True
            self.lock_seed_button.icon = ft.Icons.LOCK_OPEN
            settings_services.set_generation_value("random_seed", True)
            self.seed_field.disabled = True

        else:
            self.random_seed = False
            self.lock_seed_button.icon = ft.Icons.LOCK
            settings_services.set_generation_value("random_seed", False)
            self.seed_field.disabled = False

        self.page.update()

    def _go_to_main(self, e):
        self.page.go("/main")
        settings_services.save_configs()

    def _on_swap_button_clicked(self, e):
        temp = self.height_text_field.value
        self.height_text_field.value = self.width_text_field.value
        self.width_text_field.value = temp

        settings_services.set_generation_value(
            "width", int(self.width_text_field.value)
        )
        settings_services.set_generation_value(
            "height", int(self.height_text_field.value)
        )

        self.page.update()

    def _on_random_seed_clicked(self, e):
        random_seed = random.randint(0, 2**32 - 1)
        self.seed_field.value = random_seed

        settings_services.set_generation_value("last_seed", int(self.seed_field.value))

        self.page.update()

    def _on_save_image_after_generation_switch(self, e):
        if self.save_image_after_generation_switch.value:
            settings_services.set_generation_value("save_on_generate", True)

        else:
            settings_services.set_generation_value("save_on_generate", False)

    def _on_face_detailer_switch(self, e):
        if self.face_detailer_switch.value == True:
            self.face_detailer_settings_column.visible = True
            settings_services.set_generation_value("use_face_detailer", True)

        else:
            self.face_detailer_settings_column.visible = False
            settings_services.set_generation_value("use_face_detailer", False)

        self.page.update()

    def _on_connect_button_clicked(self, e):
        asyncio.run(client.check_connection())
        if client.connected:
            self.Connection_string.value = "Connected"
            self.Connection_string.color = ft.Colors.GREEN

        else:
            self.Connection_string.value = "Disconnected"
            self.Connection_string.color = ft.colors.RED

        self.page.update()
        settings_services.save_configs()
