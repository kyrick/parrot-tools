import os
from random import randint

import torch
from diffusers.pipelines.stable_diffusion import StableDiffusionPipelineOutput
from IPython.display import display  # type: ignore
from tqdm import trange  # type: ignore

from parrot_tools.generate.settings import (
    BatchSettings,
    Prompt,
    RunSettings,
)
from parrot_tools.utils.image_utils import make_images_grid


def generate_images(
    pipe,
    *,
    prompt: str,
    seed: int,
    steps: int,
    cfg_scale: float,
    height: int,
    width: int,
) -> StableDiffusionPipelineOutput:
    generator = torch.Generator("cuda").manual_seed(seed)

    res = pipe(
        prompt,
        num_inference_steps=steps,
        guidance_scale=cfg_scale,
        generator=generator,
        height=height,
        width=width,
        num_images_per_prompt=1,
    )

    return res


def run_prompts(pipe, prompts: list[Prompt], batch_settings: BatchSettings):

    # loop through prompts and generate images!
    for prompt in prompts:
        settings = RunSettings(prompt=prompt, batch=batch_settings)

        if settings.batch.save_individual_images:
            os.makedirs(settings.images_out_path, exist_ok=True)
        os.makedirs(settings.grid_path, exist_ok=True)

        run_id = prompt.run_id

        # we calculate the starting seed if no manual seed is provided
        if batch_settings.seed == -1:
            seed = randint(1, 1000000)
        else:
            seed = batch_settings.seed

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
            )
            res_images = res.images
            images += res_images

            for image in res_images:
                if settings.batch.display_individual_images:
                    display(image)
                if settings.batch.save_individual_images:
                    image.save(
                        settings.get_image_path(run_id=run_id, image_num=i)
                    )

            # we increment the seed for the next iteration
            seed += 1

        grid = make_images_grid(
            images,
            cols=settings.batch.grid_cols,
            padding=settings.batch.grid_padding,
            bg_color=settings.batch.grid_bg_color,
        )
        if settings.batch.display_grid_images:
            display(grid)
        grid.save(str(settings.get_grid_image_path(run_id=run_id)))
