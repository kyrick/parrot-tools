from parrot_tools.utils.prompt_utils import prepare_prompts_for_study


def test_prepare_prompts_for_study():

    base_prompts_block = """
    This is a test prompt
    This is another test prompt"""

    names_block = """
    Aivazovsky, Ivan
    da Vinci, Leonardo
    Friedrich\tCaspar David
    RHADS
    """

    modifiers_block = """
    synthwave
    vaporwave
    """

    append_to_all_prompts = "artstation"
    prompts = prepare_prompts_for_study(
        base_prompts_block, names_block, modifiers_block, append_to_all_prompts
    )

    assert len(prompts) == 12
    assert prompts[0].folder_name == "Aivazovsky_Ivan"
    assert prompts[0].base_filename == "Aivazovsky_Ivan"
    assert prompts[0].prompt == "This is a test prompt by Ivan Aivazovsky, artstation"
    assert (
        prompts[1].prompt
        == "This is another test prompt by Ivan Aivazovsky, artstation"
    )

    assert prompts[2].folder_name == "da_Vinci_Leonardo"
    assert prompts[2].base_filename == "da_Vinci_Leonardo"

    assert prompts[4].folder_name == "Friedrich_Caspar_David"
    assert prompts[4].base_filename == "Friedrich_Caspar_David"

    assert prompts[6].folder_name == "RHADS"
    assert prompts[6].base_filename == "RHADS"
    assert prompts[6].prompt == "This is a test prompt by RHADS, artstation"

    assert prompts[8].folder_name == "synthwave"
    assert prompts[8].base_filename == "synthwave"
    assert prompts[8].prompt == "This is a test prompt, synthwave, artstation"

    assert prompts[10].folder_name == "vaporwave"
    assert prompts[10].base_filename == "vaporwave"
    assert prompts[10].prompt == "This is a test prompt, vaporwave, artstation"
