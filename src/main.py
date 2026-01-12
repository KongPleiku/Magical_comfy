import flet as ft
from loguru import logger
from views.main_view import Main_View
from views.setting_view import Setting_View
from utils.ultis import ALL_TAGS
from services.setting_services import settings_services
from route import navigator


def main(page: ft.Page):
    navigator.set_page(page)

    page.views.append(Setting_View(page))
    page.views.append(Main_View(page))

    page.go("/main")


ft.app(main, assets_dir="assets")
