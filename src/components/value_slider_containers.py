import flet as ft
from loguru import logger


class Slider_Container_INT(ft.Container):
    def __init__(
        self,
        text: str,
        min_value: int,
        max_value: int,
        divisions: int,
        initial_value: int,
        is_float: bool = False,
        on_change = None
    ):
        self.on_change = on_change
        self.is_float = is_float
        self.text_label = ft.Text(text, expand=True)
        self.value_label = ft.Text(
            value=str(initial_value),
            width=50,
            text_align=ft.TextAlign.CENTER,
        )
        self.slider = ft.Slider(
            min=min_value,
            max=max_value,
            divisions=divisions,
            value=initial_value,
            expand=True,
            on_change=self._on_slider_change,
        )

        self.container = ft.Container(
            ft.Column(
                [
                    self.text_label,
                    ft.Row(
                        [
                            self.slider,
                            ft.Container(
                                content=self.value_label,
                                width=50,
                                height=30,
                                bgcolor=ft.Colors.ON_SURFACE_VARIANT,
                                alignment=ft.alignment.center,
                                border_radius=10,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        expand=True,
                        spacing=10,
                    ),
                ]
            )
        )

        super().__init__(content=self.container)

    def _on_slider_change(self, e):
        if self.on_change:
            self.on_change(e)

        if self.is_float:
            self.value_label.value = str(e.control.value)
        else:
            self.value_label.value = int(e.control.value)

        self.value_label.update()
