from pathlib import Path

from parrot_tools.utils.file_utils import create_abs_filepath


def test_create_abs_filepath():
    base_path = Path("/tmp")
    base_filename = "test"
    batch_num = 1
    image_num = 1
    seed = 1
    ext = "png"
    filepath = create_abs_filepath(
        base_path, base_filename, batch_num, image_num, seed, ext
    )
    assert filepath == Path("/tmp/test_0001_0001_1.png")


def test_create_abs_filepath_no_image_num():
    base_path = Path("/tmp")
    base_filename = "test"
    batch_num = 1
    seed = 1
    ext = "png"
    filepath = create_abs_filepath(
        base_path, base_filename, batch_num, seed=seed, ext=ext
    )
    assert filepath == Path("/tmp/test_0001.png")
