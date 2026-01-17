from utils.singleton import SingletonMeta
from loguru import logger

import flet as ft


class Router(metaclass=SingletonMeta):
    def __init__(self):
        self.page = None
        logger.info("Navigator initialized.")

    def set_page(self, page: ft.Page):
        self.page = page

    def go_to_main(self):
        logger.info("Going to main view.")
        if self.page:
            self.page.go("/main")
        else:
            logger.error("Page not set in Navigator.")

    def go_to_settings(self):
        if self.page:
            self.page.go("/settings")
        else:
            logger.error("Page not set in Navigator.")

    def go_to_gallery(self):
        if self.page:
            self.page.go("/gallery")
        else:
            logger.error("Page not set in Navigator.")


navigator = Router()
