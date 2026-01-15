from utils.singleton import SingletonMeta
from loguru import logger
from dataclasses import dataclass, asdict

import os
import json
from dacite import from_dict
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
storage_path = os.getenv("FLET_APP_STORAGE_DATA")


@dataclass
class Connection_setting:
    port: str
    host: str


@dataclass
class Generation_setting:
    # Basic Generation
    model_name: str

    last_seed: int
    random_seed: bool

    steps: int
    cfg: float
    sampler_name: str
    scheduler: str

    # Resolution
    width: int
    height: int

    # Saving option
    save_on_generate: bool
    use_face_detailer: bool


@dataclass
class Face_detailer_settings:
    use_face_detailer: bool
    guide_size: int
    guide_size_for: bool
    last_seed: int
    steps: int
    cfg: float
    sampler_name: str
    scheduler: str

    denoise: float
    noise_mask: bool
    force_inpaint: bool

    bbox_threshold: float
    bbox_crop_factor: float


@dataclass
class Settings:
    generation: Generation_setting
    face_detailer: Face_detailer_settings
    connection: Connection_setting


class Setting_services(metaclass=SingletonMeta):
    def __init__(self):
        self.storage_path = os.getenv("FLET_APP_STORAGE_DATA")
        self.configs_path = os.path.join(self.storage_path, "configs.json")

        self.settings = None
        self._load_configs()

        logger.info("Setting_services initialized.")

    def _init_configs(self):
        init_connection_settings = Connection_setting(port="192.168.1.1", host="8188")

        init_generation_settings = Generation_setting(
            use_face_detailer=False,
            model_name="WAI_ANI_Q8_0.gguf",
            last_seed=0,
            random_seed=False,
            steps=20,
            cfg=3.5,
            sampler_name="euler_ancestral",
            scheduler="sgm_uniform",
            width=512,
            height=512,
            save_on_generate=False,
        )

        init_face_detailer_settings = Face_detailer_settings(
            use_face_detailer=False,
            guide_size=512,
            guide_size_for=False,
            last_seed=0,
            steps=20,
            cfg=3.5,
            sampler_name="euler_ancestral",
            scheduler="sgm_uniform",
            denoise=0.5,
            noise_mask=False,
            force_inpaint=False,
            bbox_crop_factor=1.5,
            bbox_threshold=0.5,
        )

        self.settings = Settings(
            generation=init_generation_settings,
            face_detailer=init_face_detailer_settings,
            connection=init_connection_settings,
        )

        temp_dict = asdict(self.settings)

        logger.info(f"Initialized configs: {temp_dict}")
        self.save_configs()

    def _load_configs(self):
        try:
            with open(self.configs_path, "r") as f:
                data = json.load(f)

            self.settings = from_dict(data_class=Settings, data=data)
            logger.info(f"Loaded configs: {self.settings}")

        except Exception as e:
            logger.exception(
                f"Error or Missing file while loading configs from {self.configs_path}"
            )
            self._init_configs()

    def save_configs(self):
        try:
            with open(self.configs_path, "w") as f:
                json.dump(asdict(self.settings), f, indent=4)
            logger.info(f"Saved configs to {self.configs_path}")
        except:
            logger.error(f"Error while saving configs to {self.configs_path}")

    def set_generation_value(self, key: str, value: Any):
        """
        Sets a single value in Generation settings by key name.
        Example: set_generation_value("width", 1024)
        """
        if hasattr(self.settings.generation, key):
            # Optional: Add type validation here if needed
            setattr(self.settings.generation, key, value)
            self.save_configs()
            logger.info(f"Updated Generation [{key}] to {value}")
        else:
            logger.error(f"Generation setting '{key}' does not exist.")

    def get_generation_value(self, key: str) -> Any:
        """
        Gets a single value from Generation settings.
        """
        return getattr(self.settings.generation, key, None)

    def set_face_detailer_value(self, key: str, value: Any):
        """
        Sets a single value in Face Detailer settings by key name.
        Example: set_face_detailer_value("bbox_threshold", 0.6)
        """
        if hasattr(self.settings.face_detailer, key):
            setattr(self.settings.face_detailer, key, value)
            self.save_configs()
            logger.info(f"Updated Face Detailer [{key}] to {value}")
        else:
            logger.error(f"Face Detailer setting '{key}' does not exist.")

    def get_face_detailer_value(self, key: str) -> Any:
        """
        Gets a single value from Face Detailer settings.
        """
        return getattr(self.settings.face_detailer, key, None)

    def set_connection_settings(self, key: str, value: Any):
        """
        Sets a single value in Connection settings by key name.
        Example: set_connection_settings("port", 8188)
        """
        if hasattr(self.settings.connection, key):
            setattr(self.settings.connection, key, value)
            self.save_configs()
            logger.info(f"Updated Connection [{key}] to {value}")
        else:
            logger.error(f"Connection setting '{key}' does not exist.")


settings_services = Setting_services()
