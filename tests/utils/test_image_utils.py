from PIL import Image

from parrot_tools.utils.image_utils import make_image_grids


def test_make_image_grids():
    images = [Image.new("RGB", (100, 100), color="red")] * 10
    grids = make_image_grids(images, max_per_grid=6, padding=10, bg_color="black")
    assert len(grids) == 2
    assert grids[0].size == (340, 230)
    assert grids[1].size == (340, 230)
