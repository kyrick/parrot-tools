from enum import Enum
from pathlib import Path

from pydantic import BaseModel


class ImageFormat(str, Enum):
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"


class Prompt(BaseModel):
    folder_name: str
    base_filename: str
    prompt: str
    run_id: int


class BatchSettings(BaseModel):
    batch_size: int
    batch_name: str
    base_path: Path

    steps: int = 50
    cfg_scale: float = 7.5
    seed: int = -1

    display_individual_images: bool = False
    image_ext: ImageFormat = ImageFormat.JPEG
    image_w: int = 512
    image_h: int = 512

    grid_cols: int = 3
    grid_padding: int = 5
    grid_bg_color: str = "black"
    display_grid_images: bool = True
    save_individual_images: bool = False


class RunSettings(BaseModel):
    prompt: Prompt
    batch: BatchSettings

    @property
    def images_out_path(self) -> Path:
        return self.batch.base_path / self.batch.batch_name / self.prompt.folder_name

    def get_image_path(self, *, run_id: int, image_num: int) -> Path:
        return (
            self.images_out_path
            / f"{self.prompt.base_filename}_{run_id:0>4d}_{image_num:0>4d}.{self.batch.image_ext}"
        )

    @property
    def grid_path(self) -> Path:
        batch_path = self.batch.base_path / self.batch.batch_name
        return batch_path / "grids"

    def get_grid_image_path(self, *, run_id: int) -> Path:
        return (
            self.grid_path
            / f"{self.prompt.base_filename}_{run_id}.{self.batch.image_ext}"
        )
