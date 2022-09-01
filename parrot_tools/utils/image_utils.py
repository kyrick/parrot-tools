from typing import List, Optional

from PIL import Image


def make_image_grids(
    images: List[Image.Image],
    cols: Optional[int] = None,
    max_per_grid: int = 6,
    padding: int = 10,
    bg_color: str = "black",
) -> List[Image.Image]:
    """Make a list of image grids from a list of images."""

    # calc columns and rows from max_per_grid with max cols
    if cols:
        rows = max_per_grid // cols
    else:
        cols = max_per_grid // 2
        rows = max_per_grid // cols

    # split images into sublists of max_per_grid
    image_sublists = [
        images[i : i + max_per_grid] for i in range(0, len(images), max_per_grid)
    ]

    width, height = images[0].size

    total_w = cols * width + padding * (cols + 1)
    total_h = rows * height + padding * (rows + 1)

    grids = []
    for image_sublist in image_sublists:
        grid = Image.new("RGB", size=(total_w, total_h), color=bg_color)
        for j, image in enumerate(image_sublist):
            x = j % cols
            y = j // cols
            grid.paste(
                image, (x * width + padding * (x + 1), y * height + padding * (y + 1))
            )
        grids.append(grid)

    return grids
