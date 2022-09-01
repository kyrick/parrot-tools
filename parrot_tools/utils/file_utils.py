from pathlib import Path
from typing import Optional


def create_abs_filepath(
    base_path: Path,
    base_filename: str,
    batch_num: int,
    image_num: Optional[int] = None,
    seed: Optional[int] = None,
    ext: str = "png",
) -> Path:

    if image_num is not None:
        return (
            base_path
            / f"{base_filename}_{batch_num:0>4d}_{image_num:0>4d}_{seed}.{ext}"
        )

    return base_path / f"{base_filename}_{batch_num:0>4d}.{ext}"
