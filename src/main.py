import flet as ft
from loguru import logger
from views.main_view import Main_View
from views.setting_view import Setting_View
from views.gallery_view import Gallery_View
from utils.ultis import ALL_TAGS, API_JSON
from services.setting_services import settings_services
from services.client_services import client
from route import navigator


def main(page: ft.Page):
    navigator.set_page(page)

    main_view = Main_View(page)
    setting_view = Setting_View(page)
    gallery_view = Gallery_View(page)

    def route_change(route):
        page.views.clear()
        if page.route == "/main":
            page.views.append(main_view)
        elif page.route == "/settings":
            page.views.append(setting_view)

        elif page.route == "/gallery":
            page.views.append(gallery_view)

        page.update()

    page.on_route_change = route_change
    page.go("/main")


ft.app(main, assets_dir="assets")
