from PIL import Image

from parrot_tools.utils.image_utils import make_image_grids


def test_make_image_grids():
    images = [Image.new("RGB", (100, 100), color="red")] * 10
    grids = make_image_grids(images, max_per_grid=6, padding=10, bg_color="black")
    assert len(grids) == 2
    assert grids[0].size == (340, 230)
    assert grids[1].size == (340, 230)


def test_make_image_grids_with_cols_less_than_zero():
    """Test that cols are not used if less than zero."""

    images = [Image.new("RGB", (100, 100), color="red")] * 10
    grids = make_image_grids(
        images, cols=-1, max_per_grid=6, padding=10, bg_color="black"
    )
    assert len(grids) == 2
    assert grids[0].size == (340, 230)
    assert grids[1].size == (340, 230)


def test_make_image_grids_with_cols_greater_than_max_per_grid():
    """Test that cols are not used if greater than max_per_grid."""

    images = [Image.new("RGB", (100, 100), color="red")] * 10
    grids = make_image_grids(
        images, cols=7, max_per_grid=6, padding=10, bg_color="black"
    )
    assert len(grids) == 2
    assert grids[0].size == (340, 230)
    assert grids[1].size == (340, 230)


def test_make_image_grids_with_cols():
    """Test that cols are used if valid."""

    images = [Image.new("RGB", (100, 100), color="red")] * 10
    grids = make_image_grids(
        images, cols=2, max_per_grid=6, padding=10, bg_color="black"
    )
    assert len(grids) == 2
    assert grids[0].size == (230, 340)
    assert grids[1].size == (230, 340)
