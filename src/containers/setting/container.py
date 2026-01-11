import flet as ft


class setting_panel(ft.Container):
    def __init__(self):
        super().__init__()
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Generation", icon=ft.icons.TUNE),
                ft.Tab(text="Connection", icon=ft.icons.LINK),
                ft.Tab(text="Debug", icon=ft.icons.BUG_REPORT),
            ],
        )

        self.content = ft.Column(
            controls=[
                ft.Container(
                    width=40,
                    height=5,
                    bgcolor=ft.colors.GREY_600,
                    border_radius=10,
                    alignment=ft.alignment.center,
                ),
                ft.Row(
                    controls=[
                        ft.Text("Settings", size=20, weight="bold"),
                        ft.IconButton(ft.icons.CLOSE),
                    ],
                    alignment="spaceBetween",
                ),
                ft.Divider(color=ft.colors.GREY_800),
                self.tabs,
            ]
        )
