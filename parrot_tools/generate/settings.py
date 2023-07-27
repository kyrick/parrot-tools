from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class ImageFormat(str, Enum):
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"


class Prompt(BaseModel):
    folder_name: Optional[str] = None
    base_filename: str
    prompt: str


class BatchSettings(BaseModel):
    batch_size: int
    batch_name: str
    base_path: Path

    steps: int = 50
    cfg_scale: float = 7.5
    seed: int = -1
    NSFW_retry: int = 0

    display_individual_images: bool = True
    image_ext: ImageFormat = ImageFormat.JPEG
    image_w: int = 512
    image_h: int = 512

    make_grid: bool = False
    grid_cols: int = -1
    grid_max_images: int = 6
    grid_padding: int = 5
    grid_bg_color: str = "black"
    display_grid_images: bool = True

    num_images_per_prompt: int = 1


class RunSettings(BaseModel):
    prompt: Prompt
    batch: BatchSettings

    @property
    def images_out_path(self) -> Path:
        folder_name = self.prompt.folder_name if self.prompt.folder_name else ""
        return self.batch.base_path / self.batch.batch_name / folder_name

    @property
    def settings_path(self) -> Path:
        return self.images_out_path / "settings"

    def get_image_path(self, *, run_id: int, seed: int, image_num: int) -> Path:
        return (
            self.images_out_path
            / f"{self.prompt.base_filename}_{run_id:0>4d}_{image_num:0>4d}_{seed}.{self.batch.image_ext}"
        )

    def save(self, run_id: int):
        settings_filename = self.settings_path / f"settings_{run_id:0>4d}.txt"
        with open(settings_filename, "w") as f:
            f.write(self.model_dump_json(indent=4))

    @property
    def grid_path(self) -> Path:
        return self.images_out_path / "grids"

    def get_grid_image_path(self, *, run_id: int, grid_num: int) -> Path:
        return (
            self.grid_path
            / f"{self.prompt.base_filename}_{run_id:0>4d}_{grid_num:0>4d}.{self.batch.image_ext}"
        )
