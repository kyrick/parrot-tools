from PIL import Image

from parrot_tools.utils.image_utils import make_images_grid


def test_make_images_grid():
    images = [Image.new("RGB", (100, 100), color="red")] * 6
    grid = make_images_grid(images, cols=3, padding=10, bg_color="black")
    assert grid.size == (340, 230)