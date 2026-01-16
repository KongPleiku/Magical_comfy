from utils.singleton import SingletonMeta
from utils.ultis import API_JSON

from services.client_services import client
from services.setting_services import settings_services

from loguru import logger
import json


class Generation_services:
    def __init__(self):
        self.api = API_JSON

        self.api["8"]["inputs"]["width"] = settings_services.settings.generation.width
        self.api["8"]["inputs"]["height"] = settings_services.settings.generation.height

        self.api["7"]["inputs"][
            "seed"
        ] = settings_services.settings.generation.last_seed
        self.api["7"]["inputs"]["steps"] = settings_services.settings.generation.steps
        self.api["7"]["inputs"]["cfg"] = settings_services.settings.generation.cfg
        self.api["7"]["inputs"][
            "sampler_name"
        ] = settings_services.settings.generation.sampler_name
        self.api["7"]["inputs"][
            "scheduler"
        ] = settings_services.settings.generation.scheduler

        self.api["13"]["inputs"][
            "seed"
        ] = settings_services.settings.generation.last_seed
        self.api["13"]["inputs"][
            "steps"
        ] = settings_services.settings.face_detailer.steps
        self.api["13"]["inputs"]["cfg"] = settings_services.settings.face_detailer.cfg
        self.api["13"]["inputs"][
            "sampler_name"
        ] = settings_services.settings.face_detailer.sampler_name
        self.api["13"]["inputs"][
            "scheduler"
        ] = settings_services.settings.face_detailer.scheduler
        self.api["13"]["inputs"][
            "denoise"
        ] = settings_services.settings.face_detailer.denoise
        self.api["13"]["inputs"][
            "force_inpaint"
        ] = settings_services.settings.face_detailer.force_inpaint
        self.api["13"]["inputs"][
            "noise_mask"
        ] = settings_services.settings.face_detailer.noise_mask
        self.api["13"]["inputs"][
            "bbox_threshold"
        ] = settings_services.settings.face_detailer.bbox_threshold
        self.api["13"]["inputs"][
            "bbox_crop_factor"
        ] = settings_services.settings.face_detailer.bbox_crop_factor

        self.payload = {"client_id": str(client.current_client_id), "prompt": self.api}

    def generate(self, prompt):
        self.api["4"]["inputs"]["text"] = prompt

        data = json.dumps(self.payload).encode("utf-8")
        url = f"{client._get_base_url()}/prompt"

        logger.info(f"data: {data}")

        client.client.post(
            url=url, data=data, headers={"Content-Type": "application/json"}
        )
