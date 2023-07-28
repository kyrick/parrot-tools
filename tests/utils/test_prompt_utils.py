from parrot_tools.utils.prompt_utils import (
    prepare_prompts_for_study,
    format_base_filename
)


def test_prepare_prompts_for_study():

    base_prompts_block = """
    This is a test prompt
    This is another test prompt"""

    names_block = """
    Aivazovsky, Ivan
    da Vinci, Leonardo
    Friedrich\tCaspar David
    RHADS
    Gediminas Pranckevicius
    """

    modifiers_block = """
    synthwave
    vaporwave
    """

    append_to_all_prompts = "artstation"
    prompts = prepare_prompts_for_study(
        base_prompts_block, names_block, modifiers_block, append_to_all_prompts
    )

    assert len(prompts) == 14
    assert prompts[0].folder_name == "Ivan_Aivazovsky"
    assert prompts[0].base_filename == "Ivan_Aivazovsky"
    assert prompts[0].prompt == "This is a test prompt by Ivan Aivazovsky, artstation"
    assert (
        prompts[1].prompt
        == "This is another test prompt by Ivan Aivazovsky, artstation"
    )

    assert prompts[2].folder_name == "Leonardo_da_Vinci"
    assert prompts[2].base_filename == "Leonardo_da_Vinci"

    assert prompts[4].folder_name == "Caspar_David_Friedrich"
    assert prompts[4].base_filename == "Caspar_David_Friedrich"

    assert prompts[6].folder_name == "RHADS"
    assert prompts[6].base_filename == "RHADS"
    assert prompts[6].prompt == "This is a test prompt by RHADS, artstation"

    assert prompts[8].folder_name == "Gediminas_Pranckevicius"
    assert prompts[8].base_filename == "Gediminas_Pranckevicius"
    assert (
        prompts[8].prompt
        == "This is a test prompt by Gediminas Pranckevicius, artstation"
    )

    assert prompts[10].folder_name == "synthwave"
    assert prompts[10].base_filename == "synthwave"
    assert prompts[10].prompt == "This is a test prompt, synthwave, artstation"

    assert prompts[12].folder_name == "vaporwave"
    assert prompts[12].base_filename == "vaporwave"
    assert prompts[12].prompt == "This is a test prompt, vaporwave, artstation"


def test_prepare_prompts_for_study_with_empty_names_block():

    base_prompts_block = """
    This is a test prompt
    This is another test prompt"""

    names_block = ""

    modifiers_block = """
    synthwave
    """

    append_to_all_prompts = "artstation"
    prompts = prepare_prompts_for_study(
        base_prompts_block, names_block, modifiers_block, append_to_all_prompts
    )

    assert len(prompts) == 2
    assert prompts[0].folder_name == "synthwave"
    assert prompts[0].base_filename == "synthwave"
    assert prompts[0].prompt == "This is a test prompt, synthwave, artstation"
    assert prompts[1].prompt == "This is another test prompt, synthwave, artstation"


def test_prepare_prompts_for_study_with_empty_modifiers_block():

    base_prompts_block = """
    This is a test prompt
    This is another test prompt"""

    names_block = """
    Aivazovsky, Ivan
    """

    modifiers_block = ""

    append_to_all_prompts = "artstation"

    prompts = prepare_prompts_for_study(
        base_prompts_block, names_block, modifiers_block, append_to_all_prompts
    )

    assert len(prompts) == 2
    assert prompts[0].folder_name == "Ivan_Aivazovsky"
    assert prompts[0].base_filename == "Ivan_Aivazovsky"
    assert prompts[0].prompt == "This is a test prompt by Ivan Aivazovsky, artstation"
    assert (
        prompts[1].prompt
        == "This is another test prompt by Ivan Aivazovsky, artstation"
    )


def test_prepare_prompts_for_study_with_empty_append_to_all_prompts():

    base_prompts_block = """
    This is a test prompt
    This is another test prompt"""

    names_block = """
    Aivazovsky, Ivan
    """

    modifiers_block = ""

    append_to_all_prompts = ""

    prompts = prepare_prompts_for_study(
        base_prompts_block, names_block, modifiers_block, append_to_all_prompts
    )

    assert len(prompts) == 2
    assert prompts[0].folder_name == "Ivan_Aivazovsky"
    assert prompts[0].base_filename == "Ivan_Aivazovsky"
    assert prompts[0].prompt == "This is a test prompt by Ivan Aivazovsky"
    assert prompts[1].prompt == "This is another test prompt by Ivan Aivazovsky"


def test_format_base_filename():
    style_name = "Aivazovsky, Ivan"
    base_filename = format_base_filename(style_name)
    assert base_filename == "Ivan_Aivazovsky"


def test_format_base_filename_no_comma():
    style_name = "Ivan Aivazovsky"
    base_filename = format_base_filename(style_name)
    assert base_filename == "Ivan_Aivazovsky"


def test_format_base_filename_with_period():
    style_name = "Aivazovsky, Ivan."
    base_filename = format_base_filename(style_name)
    assert base_filename == "Ivan_Aivazovsky"


def test_format_base_filename_with_comma_and_blank():
    style_name = ", RHADS"
    base_filename = format_base_filename(style_name)
    assert base_filename == "RHADS"

def test_format_base_filename_with_single_name():
    style_name = "RHADS"
    base_filename = format_base_filename(style_name)
    assert base_filename == "RHADS"

def test_format_base_filename_with_na():
    style_name = "N/A, Ivan"
    base_filename = format_base_filename(style_name)
    assert base_filename == "Ivan"

    style_name = "n/a, Ivan"
    base_filename = format_base_filename(style_name)
    assert base_filename == "Ivan"