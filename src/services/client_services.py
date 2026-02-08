import httpx
import asyncio
from loguru import logger
from services.setting_services import settings_services
from services.event_bus import event_bus
from utils.singleton import SingletonMeta


class Comfy_Client(metaclass=SingletonMeta):
    def __init__(self):
        self.connected = False
        self.base_url = self._get_base_url()
        self.client = httpx.Client(base_url=self.base_url, timeout=30.0)
        logger.info(f"Comfy_Client initialized with base_url: {self.base_url}")

        self.connected = self.check_connection()

    def set_connected(self, connected: bool):
        self.connected = connected
        event_bus.emit("connection_status_changed", self.connected)

    def _get_base_url(self):
        host = settings_services.settings.connection.host
        port = settings_services.settings.connection.port
        return f"http://{host}:{port}"

    def check_connection(self):
        try:
            self.base_url = self._get_base_url()
            response = self.client.get("/queue")
            response.raise_for_status()
            logger.info("Successfully connected to ComfyUI.")
            self.set_connected(True)
            return True
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error checking connection: {e}")
            self.set_connected(False)
            return False
        except httpx.RequestError as e:
            logger.error(f"Request error checking connection: {e}")
            self.set_connected(False)
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred while checking connection: {e}")
            self.set_connected(False)
            return False


client = Comfy_Client()
