import flet as ft
from loguru import logger
from views.main_view import Main_View
from views.setting_view import Setting_View
from views.gallery_view import Gallery_View
from utils.ultis import ALL_TAGS
from services.setting_services import settings_services
from services.client_services import client
from route import navigator


def main(page: ft.Page):
    navigator.set_page(page)

    def route_change(route):
        page.views.clear()
        if page.route == "/main":
            page.views.append(Main_View(page))
        elif page.route == "/settings":
            page.views.append(Setting_View(page))

        elif page.route == "/gallery":
            page.views.append(Gallery_View(page))

        page.update()

    page.on_route_change = route_change
    page.go("/main")


ft.app(main, assets_dir="assets")
