import os
from glob import glob
from pathlib import Path
from random import randint

import torch
from diffusers.pipelines.stable_diffusion import StableDiffusionPipelineOutput
from IPython.display import display  # type: ignore
from PIL import Image
from torch import autocast
from tqdm import trange  # type: ignore

from parrot_tools.generate.settings import (
    BatchSettings,
    Prompt,
    RunSettings,
)
from parrot_tools.utils.image_utils import make_image_grids


def generate_images(
    pipe,
    *,
    prompt: str,
    seed: int,
    steps: int,
    cfg_scale: float,
    height: int,
    width: int,
    num_images_per_prompt: int = 1,
) -> StableDiffusionPipelineOutput:
    generator = torch.Generator("cuda").manual_seed(seed)

    res = pipe(
        prompt,
        num_inference_steps=steps,
        guidance_scale=cfg_scale,
        generator=generator,
        height=height,
        width=width,
        num_images_per_prompt=num_images_per_prompt,
    )

    return res


def get_run_id(settings_folder: Path) -> int:
    files = glob(f"{settings_folder}/settings*.txt")

    files = sorted(files)

    # we parse the batch number from settings file names
    # settings_batchnum.txt
    if files:
        return int(files[-1].split("_")[-1].split(".")[0]) + 1
    return 0


def run_prompts(pipe, prompts: list[Prompt], batch_settings: BatchSettings):

    # loop through prompts and generate images!
    for prompt in prompts:
        settings = RunSettings(prompt=prompt, batch=batch_settings)

        os.makedirs(settings.images_out_path, exist_ok=True)
        os.makedirs(settings.settings_path, exist_ok=True)
        os.makedirs(settings.grid_path, exist_ok=True)

        run_id = get_run_id(settings.settings_path)

        settings.save(run_id)

        print("starting run id:", run_id)

        # we calculate the starting seed if no manual seed is provided
        seed = batch_settings.seed
        if batch_settings.seed is None or batch_settings.seed < 0:
            seed = randint(1, 1000000)

        print("running:", prompt.prompt)

        images = []
        for i in trange(settings.batch.batch_size):
            res = generate_images(
                pipe,
                prompt=prompt.prompt,
                seed=seed,
                steps=settings.batch.steps,
                cfg_scale=settings.batch.cfg_scale,
                height=settings.batch.image_h,
                width=settings.batch.image_w,
                num_images_per_prompt=settings.batch.num_images_per_prompt,
            )
            res_images = res.images
            final_seeds = [
                seed + j for j in range(settings.batch.num_images_per_prompt)
            ]
            images += res_images

            if settings.batch.display_individual_images:
                for image, seed in zip(res_images, final_seeds):
                    print(f"seed={seed}")
                    display(image)
            for image, seed in zip(res_images, final_seeds):
                image.save(
                    settings.get_image_path(run_id=run_id, image_num=i, seed=seed)
                )

            # we increment the seed for the next iteration
            seed += settings.batch.num_images_per_prompt

        if settings.batch.make_grid:
            # limit to batch size
            images = images[: settings.batch.batch_size]

            grids = make_image_grids(
                images,
                cols=settings.batch.grid_cols,
                max_per_grid=settings.batch.grid_max_images,
                padding=settings.batch.grid_padding,
                bg_color=settings.batch.grid_bg_color,
            )
            for i, grid in enumerate(grids):
                if settings.batch.display_grid_images:
                    display(grid)
                grid.save(str(settings.get_grid_image_path(grid_num=run_id)))
