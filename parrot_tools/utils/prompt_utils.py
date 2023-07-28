from __future__ import annotations

from parrot_tools.generate.settings import Prompt


def _parse_name(name: str) -> str:
    """Parse name into format last, first"""
    name = name.replace("n/a", "").replace("N/A", "").strip()
    name = name.replace("\t", ",").strip()
    if "," not in name:
        # if space in name, assume it's a first name
        if " " in name:
            # return last, first
            return f"{name.split(' ')[-1]}, {' '.join(name.split(' ')[:-1])}"
        return f", {name}"
    return name


def _format_name_for_prompt(name: str) -> str:
    """Format style name for prompt.

    Args:
        style_name (str): could be a person's name such as "da Vinci, Leonardo" or a modifier like "vaporwave"

    Returns:
        str: formatted style name
    """

    if "," not in name:
        return name

    # if comma in name, assume it's a person's name
    last, first = name.strip().split(",")
    last = last.strip()
    first = first.strip()
    if last:
        return f"{first.strip()} {last.strip()}"
    # if no last name, just return the first name
    return first

def format_base_filename(style_name: str) -> str:
    """Format modifier for a filename.
    If this is a person's name respect first and last name"""

    # strip period which could conflict with filename and replace tabs with commas
    style_name = style_name.replace(".", "")

    style_name = style_name.replace("N/A", "").replace("n/a", "")

    # if there is no comma, just return the name
    if "," not in style_name:
        return style_name.replace(" ", "_")

    # if there is a comma, assume it's a person's name
    last, first = style_name.split(",")
    parts = [part.strip() for part in first.split() + last.split() if part.strip()]

    return "_".join(parts)

def prepare_prompts_for_study(
    base_prompts_block: str,
    names_block: str,
    modifiers_block: str,
    append_to_all_prompts: str,
) -> list[Prompt]:
    """Prepare prompts for study.

    Args:
        base_prompts_block (str): block of prompts separated by newlines
        names_block (str): block of names separated by newlines
        modifiers_block (str): block of modifiers separated by newlines
        append_to_all_prompts (str): a string to append to all prompts

    Returns:
        list[Prompt]: List of prompts to study
    """

    if append_to_all_prompts and not append_to_all_prompts.startswith(","):
        append_to_all_prompts = ", " + append_to_all_prompts

    names_list = [_parse_name(x) for x in names_block.splitlines() if x.strip()]
    modifiers_list = [x.strip() for x in modifiers_block.splitlines() if x.strip()]
    base_prompts = [x.strip() for x in base_prompts_block.splitlines() if x.strip()]

    # build up list of prompts to run
    artist_prompts = [
        Prompt(
            folder_name=format_base_filename(name),
            base_filename=format_base_filename(name),
            prompt=f"{b} by {_format_name_for_prompt(name)}{append_to_all_prompts}",
            run_id=run_id,
        )
        for name in names_list
        for run_id, b in enumerate(base_prompts)
    ]

    modifier_prompts = [
        Prompt(
            folder_name=format_base_filename(modifier),
            base_filename=format_base_filename(modifier),
            prompt=f"{b}, {modifier}{append_to_all_prompts}",
            run_id=run_id,
        )
        for modifier in modifiers_list
        for run_id, b in enumerate(base_prompts)
    ]

    return artist_prompts + modifier_prompts
