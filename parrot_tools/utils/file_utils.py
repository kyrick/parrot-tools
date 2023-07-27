from pathlib import Path
from typing import Optional


def get_abs_filepath(
    base_path: Path,
    base_filename: str,
    batch_num: int,
    image_num: Optional[int] = None,
    seed: Optional[int] = None,
    ext: str = "png",
) -> Path:

    if image_num is not None:
        filename = f"{base_filename}_{batch_num:0>4d}_{image_num:0>4d}_{seed}.{ext}"
        return base_path / filename

    return base_path / f"{base_filename}_{batch_num:0>4d}.{ext}"


def format_base_filename(style_name: str) -> str:
    """Format modifier for a filename.
    If this is a person's name respect first and last name"""

    # strip period which could conflict with filename and replace tabs with commas
    style_name = style_name.replace(".", "")

    # if there is no comma, just return the name
    if "," not in style_name:
        return style_name.replace(" ", "_")

    # if there is a comma, assume it's a person's name
    last, first = style_name.split(",")
    parts = [part.strip() for part in first.split() + last.split() if part.strip()]

    return "_".join(parts)
