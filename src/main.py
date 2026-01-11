import flet as ft
from loguru import logger
from views.main_view import Main_View
from utils.ultis import ALL_TAGS


def main(page: ft.Page):
    def router(route):
        page.views.clear()
        logger.info(f"Navigating to {page.route}")

        if page.route == "/main":
            main = Main_View(page)
            page.views.append(main)

        page.update()

    page.on_route_change = router
    page.go("/main")


ft.app(main, assets_dir="assets")
