import httpx
import websocket
import uuid
from loguru import logger
from services.setting_services import settings_services
from utils.singleton import SingletonMeta
from utils.event_bus import event_bus


class Comfy_Client(metaclass=SingletonMeta):
    def __init__(self):
        self.connected = False

        self.base_url = self._get_base_url()
        self.client = httpx.Client(base_url=self.base_url, timeout=30.0)

        self.websocket_client = websocket.WebSocket()
        self.current_client_id = uuid.uuid4()

        logger.info(f"Comfy_Client initialized with base_url: {self.base_url}")

        self.check_connection()
        self._create_websocket_connection()

    def _get_base_url(self):
        host = settings_services.settings.connection.host
        port = settings_services.settings.connection.port
        url = f"http://{host}:{port}"
        logger.info(f"url: {url}")
        return url

    def _get_ws_url(self):
        self.current_client_id = uuid.uuid4()

        host = settings_services.settings.connection.host
        port = settings_services.settings.connection.port

        server_address = f"{host}:{port}"
        logger.info(server_address)

        ws_url = f"ws://{server_address}/ws?clientId={self.current_client_id}"
        logger.info(f"ws_connection: {ws_url}")
        return ws_url

    def _create_http_connection(self):
        try:
            self.base_url = self._get_base_url()
            self.client = httpx.Client(base_url=self.base_url, timeout=30.0)
            response = self.client.get("/queue")
            response.raise_for_status()
            logger.info("Successfully connected to ComfyUI.")
            return True
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error checking connection: {e}")
            return False
        except httpx.RequestError as e:
            logger.error(f"Request error checking connection: {e}")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred while checking connection: {e}")
            return False

    def _create_websocket_connection(self):
        try:
            url = self._get_ws_url()
            self.websocket_client.connect(url=url)

            return True

        except Exception as e:
            logger.error(
                f"An unexpected error occured while creating websocket connection: {e}"
            )

    def check_connection(self):
        if self._create_http_connection() and self._create_websocket_connection():
            self.connected = True

        else:
            self.connected = False

    def cancel_generation(self):
        """Sends a request to interrupt the current generation."""
        try:
            response = self.client.post("/interrupt")
            response.raise_for_status()
            logger.info("Successfully sent interruption request.")

            event_bus.publish("on_cancel")
            return True
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error sending interruption request: {e}")
            return False
        except httpx.RequestError as e:
            logger.error(f"Request error sending interruption request: {e}")
            return False

    def close_websocket(self):
        """Closes the websocket connection if it is open."""
        if self.websocket_client.connected:
            self.websocket_client.close()
            logger.info("WebSocket connection closed by client.")


client = Comfy_Client()
