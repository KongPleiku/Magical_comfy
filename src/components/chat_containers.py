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

        self.suggestion_list = ft.ListView(spacing=0, padding=0)

        # Temparory_add data for list_view
        count = 1

        for i in range(0, 10):
            self.suggestion_list.controls.append(
                ft.Text(f"Line {count}", color=ft.Colors.ON_SECONDARY)
            )
            count += 1

        # Temparory add suggestion view
        self.suggestion_container = ft.Container(
            content=self.suggestion_list,
            bgcolor=ft.colors.GREY_900,
            border_radius=15,
            height=20,  # Change this to 0 to hide
            opacity=1,  # Change this to 0 to hide
            animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT),
            animate_opacity=200,
            margin=ft.margin.only(bottom=10, left=10, right=10),
        )

        # Removed 'expand=True' from Row.
        # The TextField already has 'expand=True', so it will take up
        # all available horizontal space inside the bar.
        self.prompt_section = ft.Row(
            controls=[self.prompt_field, self.action_button],
        )

        self.wrapper = ft.Column(
            controls=[self.suggestion_container, self.prompt_section],
            expand=True,
            spacing=0,
        )

        super().__init__(
            content=self.wrapper,
            bottom=0,
            left=0,
            right=0,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
        )
