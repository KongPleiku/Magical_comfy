import flet as ft
from utils.event_bus import event_bus


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

        event_bus.subscribe("on_generate", self.on_generate_state)
        event_bus.subscribe("image_downloaded", self.on_success_generate_state)
        event_bus.subscribe("on_cancel", self.on_cancel_state)

    def on_generate_state(self, prompt_id):
        self.status_text.color = ft.Colors.YELLOW_500
        self.status_text.value = "Previewing"

        self.action_text.color = ft.Colors.BLUE_500
        self.action_text.value = "On Generation"

        self.update()

    def on_success_generate_state(self, a):
        self.status_text.color = ft.Colors.GREEN
        self.status_text.value = "Successful"

        self.action_text.color = ft.Colors.WHITE
        self.action_text.value = "Idle"

        self.update()

    def on_cancel_state(self):
        self.status_text.color = ft.Colors.RED
        self.status_text.value = "Cancelled"

        self.action_text.color = ft.Colors.WHITE
        self.action_text.value = "Idle"

        self.update()
