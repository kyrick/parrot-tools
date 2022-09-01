from pathlib import Path

from parrot_tools.utils.file_utils import format_base_filename, get_abs_filepath


def test_create_abs_filepath():
    base_path = Path("/tmp")
    base_filename = "test"
    batch_num = 1
    image_num = 1
    seed = 1
    ext = "png"
    filepath = get_abs_filepath(
        base_path, base_filename, batch_num, image_num, seed, ext
    )
    assert filepath == Path("/tmp/test_0001_0001_1.png")


def test_create_abs_filepath_no_image_num():
    base_path = Path("/tmp")
    base_filename = "test"
    batch_num = 1
    seed = 1
    ext = "png"
    filepath = get_abs_filepath(base_path, base_filename, batch_num, seed=seed, ext=ext)
    assert filepath == Path("/tmp/test_0001.png")


def test_format_base_filename():
    style_name = "Aivazovsky, Ivan"
    base_filename = format_base_filename(style_name)
    assert base_filename == "Aivazovsky_Ivan"


def test_format_base_filename_no_comma():
    style_name = "Aivazovsky Ivan"
    base_filename = format_base_filename(style_name)
    assert base_filename == "Aivazovsky_Ivan"


def test_format_base_filename_with_period():
    style_name = "Aivazovsky, Ivan."
    base_filename = format_base_filename(style_name)
    assert base_filename == "Aivazovsky_Ivan"


def test_format_base_filename_with_comma_and_blank():
    style_name = ", RHADS"
    base_filename = format_base_filename(style_name)
    assert base_filename == "RHADS"
