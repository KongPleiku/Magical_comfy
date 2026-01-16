from utils.singleton import SingletonMeta
from utils.ultis import API_JSON

from services.client_services import client
from services.setting_services import settings_services

from loguru import logger
import json
import websocket
from typing import Callable


# Constants for node IDs to improve readability
EMPTY_LATENT_IMAGE_NODE = "8"
KSAMPLER_NODE = "7"
FACE_DETAILER_NODE = "13"
PROMPT_NODE = "4"


class GenerationService:
    def __init__(self):
        self.api = API_JSON
        self.payload = {"client_id": str(client.current_client_id), "prompt": self.api}
        self._update_generation_settings()
        self._update_face_detailer_settings()

    def _update_generation_settings(self):
        """Updates the generation settings in the API payload."""
        generation_settings = settings_services.settings.generation
        self.api[EMPTY_LATENT_IMAGE_NODE]["inputs"]["width"] = generation_settings.width
        self.api[EMPTY_LATENT_IMAGE_NODE]["inputs"][
            "height"
        ] = generation_settings.height

        sampler_settings = self.api[KSAMPLER_NODE]["inputs"]
        sampler_settings["seed"] = generation_settings.last_seed
        sampler_settings["steps"] = generation_settings.steps
        sampler_settings["cfg"] = generation_settings.cfg
        sampler_settings["sampler_name"] = generation_settings.sampler_name
        sampler_settings["scheduler"] = generation_settings.scheduler

    def _update_face_detailer_settings(self):
        """Updates the face detailer settings in the API payload."""
        detailer_settings = settings_services.settings.face_detailer
        face_detailer_inputs = self.api[FACE_DETAILER_NODE]["inputs"]
        face_detailer_inputs["seed"] = settings_services.settings.generation.last_seed
        face_detailer_inputs["steps"] = detailer_settings.steps
        face_detailer_inputs["cfg"] = detailer_settings.cfg
        face_detailer_inputs["sampler_name"] = detailer_settings.sampler_name
        face_detailer_inputs["scheduler"] = detailer_settings.scheduler
        face_detailer_inputs["denoise"] = detailer_settings.denoise
        face_detailer_inputs["force_inpaint"] = detailer_settings.force_inpaint
        face_detailer_inputs["noise_mask"] = detailer_settings.noise_mask
        face_detailer_inputs["bbox_threshold"] = detailer_settings.bbox_threshold
        face_detailer_inputs["bbox_crop_factor"] = detailer_settings.bbox_crop_factor

    def generate(self, prompt: str, binary_callback: Callable[[bytes], None] = None):
        """Generates an image based on the provided prompt and waits for completion."""
        # Ensure websocket is connected and client_id is up-to-date
        if not client.websocket_client or not client.websocket_client.connected:
            client._create_websocket_connection()

        self.payload["client_id"] = str(client.current_client_id)
        self.api[PROMPT_NODE]["inputs"]["text"] = prompt

        data = json.dumps(self.payload).encode("utf-8")
        url = f"{client._get_base_url()}/prompt"

        logger.info(f"Sending generation request with prompt: {prompt}")

        response = client.client.post(
            url=url, data=data, headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        prompt_response = response.json()
        prompt_id = prompt_response.get("prompt_id")

        if not prompt_id:
            logger.error("Failed to get prompt_id from ComfyUI response.")
            return None

        logger.info(f"Prompt ID received: {prompt_id}. Waiting for completion...")
        return self._wait_for_completion(prompt_id, binary_callback=binary_callback)

    def _wait_for_completion(
        self, prompt_id: str, binary_callback: Callable[[bytes], None] = None
    ):
        """Waits for the image generation to complete via WebSocket."""
        if not client.websocket_client or not client.websocket_client.connected:
            logger.error(
                "WebSocket client is not connected at the start of _wait_for_completion."
            )
            return None

        # Set a timeout for receiving messages to prevent indefinite blocking
        # This is a workaround to ensure the thread eventually terminates
        # if the websocket connection becomes unresponsive.
        timeout_seconds = 20
        client.websocket_client.settimeout(timeout_seconds)

        while True:
            try:
                # Use a small timeout for recv to periodically check status or break loop
                message = client.websocket_client.recv()

                if isinstance(message, bytes):
                    logger.debug("Received binary WebSocket message.")
                    if binary_callback:
                        binary_callback(message)
                    continue

                message_data = json.loads(message)
                msg_type = message_data.get("type")

                if (
                    msg_type == "executed"
                    and message_data.get("data", {}).get("prompt_id") == prompt_id
                ):
                    logger.info(
                        f"Image generation completed for prompt ID: {prompt_id} (Type: {msg_type})"
                    )
                    return message_data.get("data", {}).get("output")

                elif msg_type == "execution_success":
                    logger.info(
                        f"[DEBUG] Received execution_success message. Data: {message_data}"
                    )
                    logger.info(f"[DEBUG] Currently waiting for prompt_id: {prompt_id}")

                elif msg_type == "progress":
                    logger.debug(f"Generation progress: {message_data.get('data')}")
                elif msg_type == "status":
                    logger.debug(f"Queue status: {message_data.get('data')}")
                else:
                    logger.debug(f"Received other WebSocket message: {msg_type}")

            except websocket.WebSocketConnectionClosedException:
                logger.error(
                    "WebSocket connection closed unexpectedly during generation. Aborting."
                )
                return None
            except websocket.WebSocketTimeoutException:
                logger.warning(
                    f"WebSocket message reception timed out after {timeout_seconds} seconds. Aborting."
                )
                return None
            except json.JSONDecodeError:
                logger.error(f"Failed to decode WebSocket message: {message[:100]}...")
            except Exception as e:
                logger.error(f"An error occurred while waiting for completion: {e}")
                return None
