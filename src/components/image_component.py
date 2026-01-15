import flet as ft

src = "https://picsum.photos/1080/1920"


class Image_component(ft.InteractiveViewer):
    def __init__(self):
        self.image = ft.Image(
            src="https://picsum.photos/1080/1920",
            fit=ft.ImageFit.FIT_WIDTH,
            expand=True,
        )

        super().__init__(
            content=self.image,
            expand=True,
            min_scale=1.0,
            max_scale=5.0,
            boundary_margin=ft.margin.all(5),
        )
