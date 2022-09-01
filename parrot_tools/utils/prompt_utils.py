from dataclasses import dataclass
from typing import List

from parrot_tools.utils.file_utils import format_base_filename


@dataclass(frozen=True)
class Prompt:
    name: str
    filename: str
    prompt: str


def _format_for_name(name: str) -> str:
    return _format_style_for_prompt(name).replace("by", "").replace(",", "").strip()


def _format_style_for_prompt(style_name: str) -> str:
    """Format style name for prompt.

    Args:
        style_name (str): could be a person's name such as "da Vinci, Leonardo" or a modifier like "vaporwave"

    Returns:
        str: formatted style name
    """
    last_first = style_name.strip().split(",")
    if len(last_first) == 2:
        last, first = last_first
        last = last.strip()
        first = first.strip()
        if last:
            return f" by {first.strip()} {last.strip()}"
        # if no last name, just return the first name
        return f" by {first}"
    # if no comma, just return the name
    return f", {style_name}"


def prepare_prompts_for_study(
    base_prompts_block: str,
    names_block: str,
    modifiers_block: str,
    append_to_all_prompts: str,
) -> List[Prompt]:
    """Prepare prompts for study.

    Args:
        base_prompts_block (str): block of prompts separated by newlines
        styles_block (str): block of styles separated by newlines
        append_to_all_prompts (str): a string to append to all prompts

    Returns:
        List[Prompt]: List of prompts to study
    """

    if append_to_all_prompts and not append_to_all_prompts.startswith(","):
        append_to_all_prompts = ", " + append_to_all_prompts

    def _prepare_name(name: str) -> str:
        name = name.replace("\t", ",").strip()
        if "," not in name:
            return f", {name}"
        return name

    names_list = [_prepare_name(x) for x in names_block.splitlines() if x.strip()]
    modifiers_list = [x.strip() for x in modifiers_block.splitlines() if x.strip()]
    base_prompts = [x.strip() for x in base_prompts_block.splitlines() if x.strip()]

    # build up list of prompts to run
    prompts_to_run = [
        Prompt(
            name=_format_for_name(a),
            filename=format_base_filename(a),
            prompt=f"{b}{_format_style_for_prompt(a)}{append_to_all_prompts}",
        )
        for a in names_list + modifiers_list
        for b in base_prompts
    ]

    return prompts_to_run
