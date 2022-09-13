import os
from glob import glob
from pathlib import Path
from random import randint
from typing import Any, Dict, List, Optional, Tuple

import torch
from diffusers.schedulers.scheduling_ddim import DDIMScheduler
from diffusers.schedulers.scheduling_lms_discrete import LMSDiscreteScheduler
from diffusers.schedulers.scheduling_pndm import PNDMScheduler
from IPython.display import display  # type: ignore
from PIL import Image
from torch import autocast
from tqdm import trange  # type: ignore

from parrot_tools.generate.settings import (
    BatchSettings,
    Prompt,
    RunSettings,
    SchedulerType,
)
from parrot_tools.utils.image_utils import make_image_grids


def set_scheduler(pipe, scheduler: SchedulerType):
    if scheduler == SchedulerType.DDIM:
        ddim = DDIMScheduler(
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear",
            clip_sample=False,
            set_alpha_to_one=False,
        )
        pipe.scheduler = ddim
    elif scheduler == SchedulerType.K_LMS:
        lms = LMSDiscreteScheduler(
            beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear"
        )
        pipe.scheduler = lms
    elif scheduler == SchedulerType.PNDM:
        pndm = PNDMScheduler(
            beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear"
        )
        pipe.scheduler = pndm
    else:
        raise ValueError(f"Unknown scheduler {scheduler}")


def generate_image(
    pipe,
    *,
    prompt: str,
    seed: int,
    steps: int,
    cfg_scale: float,
    height: int,
    width: int,
    init_image: Optional[Image.Image] = None,
    init_strength: float = 0.7,
    init_max_pixels: int = 262144,
) -> Dict[str, Any]:
    generator = torch.Generator("cuda").manual_seed(seed)

    with autocast("cuda"):
        res = pipe(
            prompt,
            num_inference_steps=steps,
            guidance_scale=cfg_scale,
            generator=generator,
            height=height,
            width=width,
            init_image=init_image,
            init_strength=init_strength,
            init_max_pixels=init_max_pixels,
        )

    return res


def generate_image_with_retries(
    pipe,
    *,
    prompt: str,
    start_seed: int,
    steps: int,
    cfg_scale: float,
    height: int,
    width: int,
    init_image: Optional[Image.Image] = None,
    init_strength: float = 0.7,
    init_max_pixels: int = 262144,
    retry: int = 0,
) -> Tuple[Image.Image, int]:
    image = Image.new("RGB", (width, height), "black")
    final_seed = start_seed
    for i in range(start_seed, start_seed + 1 + retry):
        res = generate_image(
            pipe,
            prompt=prompt,
            seed=i,
            steps=steps,
            cfg_scale=cfg_scale,
            height=height,
            width=width,
            init_image=init_image,
            init_strength=init_strength,
            init_max_pixels=init_max_pixels,
        )
        image = res["sample"][0]
        final_seed = i
        if not res["nsfw_content_detected"][0]:
            return image, final_seed
        print("retried!", i)

    return image, final_seed


def get_run_id(settings_folder: Path) -> int:
    files = glob(f"{settings_folder}/settings*.txt")

    files = sorted(files)

    # we parse the batch number from settings file names
    # settings_batchnum.txt
    if files:
        return int(files[-1].split("_")[-1].split(".")[0]) + 1
    return 0


def run_prompts(pipe, prompts: List[Prompt], batch_settings: BatchSettings):

    # set the scheduler on the pipe
    set_scheduler(pipe, batch_settings.scheduler)

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

            init_image = None
            # if there is an init image, we load it
            if prompt.init_image is not None:
                init_image = Image.open(prompt.init_image)

            image, seed = generate_image_with_retries(
                pipe,
                prompt=prompt.prompt,
                start_seed=seed,
                steps=settings.batch.steps,
                cfg_scale=settings.batch.cfg_scale,
                height=settings.batch.image_h,
                width=settings.batch.image_w,
                init_image=init_image,
                init_strength=prompt.init_strength,
                init_max_pixels=settings.batch.init_max_pixels,
                retry=settings.batch.NSFW_retry,
            )
            images.append(image)

            if settings.batch.display_individual_images:
                print(f"seed={seed}")
                display(image)
            image.save(settings.get_image_path(run_id=run_id, image_num=i, seed=seed))

            # we increment the seed for the next iteration
            seed += 1

        if settings.batch.make_grid:
            grids = make_image_grids(
                images,
                cols=settings.batch.grid_cols,
                max_per_grid=settings.batch.grid_max_images,
                padding=settings.batch.grid_padding,
                bg_color=settings.batch.grid_bg_color,
            )
            for i, grid in enumerate(grids):
                display(grid)
                grid.save(str(settings.get_grid_image_path(run_id=run_id, grid_num=i)))
