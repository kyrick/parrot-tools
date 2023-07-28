from __future__ import annotations

from PIL import Image


def make_images_grid(
    images: list[Image.Image],
    cols: int,
    padding: int = 10,
    bg_color: str = "black",
) -> Image.Image:
    """Make a list of image grids from a list of images."""

    total_images = len(images)

    rows = total_images // cols

    width, height = images[0].size

    total_w = cols * width + padding * (cols + 1)
    total_h = rows * height + padding * (rows + 1)

    grid = Image.new("RGB", size=(total_w, total_h), color=bg_color)
    for j, image in enumerate(images):
        x = j % cols
        y = j // cols
        grid.paste(
            image, (x * width + padding * (x + 1), y * height + padding * (y + 1))
        )

    return grid
