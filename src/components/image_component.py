import flet as ft
import base64
from utils.event_bus import event_bus
from loguru import logger


class Image_component(ft.InteractiveViewer):
    def __init__(self, page: ft.Page):
        self.page = page
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

        # Subscribe to events
        event_bus.subscribe("preview_image_received", self.update_image)
        event_bus.subscribe("image_downloaded", self.set_final_image)

    def update_image(self, image_data: bytes):
        """Updates the displayed image from binary data received via event bus."""
        if not image_data:
            logger.warning("Received empty image data, skipping update.")
            return

        # Strip the 8-byte header from the image data
        image_data = image_data[8:]

        encoded_image = base64.b64encode(image_data).decode("utf-8")

        new_image = ft.Image(
            src_base64=encoded_image,
            fit=ft.ImageFit.FIT_WIDTH,
            expand=True,
        )
        self.content = new_image
        self.image = new_image
        self.page.update()

        logger.info("Image content replaced and updated")

    def set_final_image(self, image_data: bytes):
        """Updates the displayed image from binary data received via event bus."""
        if not image_data:
            logger.warning("Received empty image data, skipping update.")
            return

        encoded_image = base64.b64encode(image_data).decode("utf-8")

        new_image = ft.Image(
            src_base64=encoded_image,
            fit=ft.ImageFit.FIT_WIDTH,
            expand=True,
        )
        self.content = new_image
        self.image = new_image
        self.page.update()

        logger.info("Image Downloaded Showing")
