import flet as ft


class Status_Container(ft.Container):
    def __init__(self):
        super().__init__()

        self.status_text = ft.Text(
            value="Ready", size=12, weight="bold", color=ft.Colors.GREEN_400
        )
        self.action_text = ft.Text(value="Idle", size=12, color=ft.Colors.WHITE70)

        self.Pack = ft.Column(
            spacing=2,
            controls=[
                ft.Row(
                    [
                        ft.Text(
                            "ACTION:",
                            size=10,
                            color=ft.colors.GREY_400,
                            weight="bold",
                        ),
                        self.action_text,
                    ],
                    spacing=5,
                ),
                ft.Row(
                    [
                        ft.Text(
                            "STATUS:",
                            size=10,
                            color=ft.colors.GREY_400,
                            weight="bold",
                        ),
                        self.status_text,
                    ],
                    spacing=5,
                ),
            ],
        )

        self.content = self.Pack
        self.top = 40
        self.left = 20
