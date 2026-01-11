import flet as ft

src = "images/sample.jpg"


class Image_component(ft.InteractiveViewer):
    def __init__(self):
        # init content image
        self.image = ft.Image(src=src)

        # init interactive view
        super().__init__(content=self.image)
        self.min_scale = 1.0
        self.max_scale = 5.0

    def change_image(self, image):
        self.image.src = image
        self.update()
