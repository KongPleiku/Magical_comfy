from utils.singleton import SingletonMeta
from loguru import logger
from dataclasses import dataclass, asdict

import os
import json
from dacite import from_dict
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
storage_path = os.getenv("FLET_APP_STORAGE_DATA")


@dataclass
class Generation_setting:
    # Basic Generation
    model_name: str
    last_seed: int
    steps: int
    cfg: float
    sampler_name: str
    scheduler: str

    # Resolution
    width: int
    height: int

    # Saving option
    save_on_generate: bool


@dataclass
class Face_detailer_settings:
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


class Setting_services(metaclass=SingletonMeta):
    def __init__(self):
        self.storage_path = os.getenv("FLET_APP_STORAGE_DATA")
        self.configs_path = os.path.join(self.storage_path, "configs.json")

        self.settings = None
        self._load_configs()

        logger.info("Setting_services initialized.")

    def _init_configs(self):
        init_generation_settings = Generation_setting(
            model_name="WAI_ANI_Q8_0.gguf",
            last_seed=0,
            steps=20,
            cfg=3.5,
            sampler_name="euler_ancestral",
            scheduler="sgm_uniform",
            width=512,
            height=512,
            save_on_generate=False,
        )

        init_face_detailer_settings = Face_detailer_settings(
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
            bbox_crop_factor=0.8,
            bbox_threshold=0.5,
        )

        self.settings = Settings(
            generation=init_generation_settings,
            face_detailer=init_face_detailer_settings,
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


settings_services = Setting_services()
