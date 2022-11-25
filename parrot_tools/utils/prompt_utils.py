import csv
import itertools
from typing import Iterator, List

from parrot_tools.generate.settings import Prompt
from parrot_tools.utils.file_utils import format_base_filename


def _parse_name(name: str) -> str:
    """Parse name into format last, first"""
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

def read_csv(csv_file_path: str) -> str:
    """Read the csv of artist names. Expects the "last, first" to be the first column. Will concat into a block of text for the next portion.

    Args:
        file_path (str): absolute/path/to/file.csv

    Returns:
        str: block of names
    """

    names_block = ""
    with open(csv_file_path) as infile:
        reader = csv.reader(infile)
        for row in reader:
            last_first = row[0]
            names_block += f"{last_first}\n"
    
    return names_block

def prepare_prompts_for_study(
    base_prompts_block: str,
    names_block: str,
    modifiers_block: str,
    append_to_all_prompts: str,
) -> List[Prompt]:
    """Prepare prompts for study.

    Args:
        base_prompts_block (str): block of prompts separated by newlines
        names_block (str): block of names separated by newlines
        modifiers_block (str): block of modifiers separated by newlines
        append_to_all_prompts (str): a string to append to all prompts

    Returns:
        List[Prompt]: List of prompts to study
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
        )
        for name in names_list
        for b in base_prompts
    ]

    modifier_prompts = [
        Prompt(
            folder_name=format_base_filename(modifier),
            base_filename=format_base_filename(modifier),
            prompt=f"{b}, {modifier}{append_to_all_prompts}",
        )
        for modifier in modifiers_list
        for b in base_prompts
    ]

    return artist_prompts + modifier_prompts


def unique_combinations(items: List[str], n) -> Iterator[List[str]]:
    """Generate every possible unique combination of elements in a list.

    Args:
        iterable (list): list of elements
        n (int): length of combinations

    Returns:
        list: list of combinations
    """
    for x in itertools.combinations(items, n):
        yield list(x)


def prepare_hybrid_prompts_for_study(
    base_prompts_block: str,
    names_block: str,
    modifiers_block: str,
    append_to_all_prompts: str,
    hybrid_count: int,
    hybridize_everything: bool = False,
) -> List[Prompt]:
    """Prepare prompts for study.

    Args:
        base_prompts_block (str): block of prompts separated by newlines
        names_block (str): block of names separated by newlines
        modifiers_block (str): block of modifiers separated by newlines
        append_to_all_prompts (str): a string to append to all prompts
        hybrid_count (int): the count of additional modifiers to add to each prompt
        hybridize_everything (bool): whether to names and modifiers

    Returns:
        List[Prompt]: List of prompts to study
    """

    # clean up the append to all prompts
    if append_to_all_prompts and not append_to_all_prompts.startswith(","):
        append_to_all_prompts = ", " + append_to_all_prompts

    # split up the blocks into lists
    names_list = [
        _format_name_for_prompt(_parse_name(x))
        for x in names_block.splitlines()
        if x.strip()
    ]
    modifiers_list = [x.strip() for x in modifiers_block.splitlines() if x.strip()]
    base_prompts = [x.strip() for x in base_prompts_block.splitlines() if x.strip()]

    # if hybridize everything, add the names and modifiers to the lists and hybridize ALL THE THINGS!!!
    if hybridize_everything:
        # build up list of prompts to run
        prompts = []

        names_list = [f"by {name}" for name in names_list]
        for items in unique_combinations(names_list + modifiers_list, hybrid_count + 1):
            for b in base_prompts:
                base_filename = format_base_filename("_".join(items))
                prompts.append(
                    Prompt(
                        folder_name=base_filename,
                        base_filename=base_filename,
                        prompt=f"{b}, {', '.join(items)}{append_to_all_prompts}",
                    )
                )
        return prompts

    # build up list of prompts to run
    prompts = []
    # add all the artist prompts
    for names in unique_combinations(names_list, hybrid_count + 1):
        base_filename = format_base_filename("_".join(names))
        for b in base_prompts:
            prompts.append(
                Prompt(
                    folder_name=base_filename,
                    base_filename=base_filename,
                    prompt=f"{b} by {' and '.join(names)}{append_to_all_prompts}",
                )
            )

    # add all the modifier prompts
    for modifiers in unique_combinations(modifiers_list, hybrid_count + 1):
        for b in base_prompts:
            base_filename = format_base_filename("_".join(modifiers))
            prompts.append(
                Prompt(
                    folder_name=base_filename,
                    base_filename=base_filename,
                    prompt=f"{b}, {', '.join(modifiers)}{append_to_all_prompts}",
                )
            )

    return prompts



if __name__ == "__main__":
    block = read_csv("data.csv")
    print(block)