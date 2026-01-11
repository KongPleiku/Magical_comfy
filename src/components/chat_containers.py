import flet as ft


class ChatBar(ft.Container):
    def __init__(self):
        self.action_button = ft.IconButton(
            icon=ft.icons.SEND, icon_color=ft.colors.WHITE, tooltip="Send"
        )

        self.prompt_field = ft.TextField(
            hint_text="Describe your image...",
            border_radius=25,
            bgcolor=ft.colors.BLACK54,
            filled=True,
            multiline=True,
            min_lines=1,
            max_lines=3,
            content_padding=ft.padding.symmetric(horizontal=20, vertical=10),
            expand=True,
            border_color=ft.colors.TRANSPARENT,
        )

        # Removed 'expand=True' from Row.
        # The TextField already has 'expand=True', so it will take up
        # all available horizontal space inside the bar.
        self.prompt_section = ft.Row(
            controls=[self.prompt_field, self.action_button],
        )

        super().__init__(
            content=self.prompt_section,
            bottom=0,
            left=0,
            right=0,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
        )
