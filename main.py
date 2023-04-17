#!/usr/bin/env python3
import logging
from pathlib import Path

import click
import jax
import numpy as np
from aicsimageio import AICSImage
from basicpy import BaSiC
from skimage.io import imsave

logger = logging.Logger("basicpy-docker-mcmicro")
logger.setLevel(logging.INFO)


def get_main_name(filename):
    candidate_exts = [".ome.tiff", ".ome.tif", ".tiff", ".tif"]
    for ext in candidate_exts:
        if ext in filename:
            return filename.replace(ext, "")
    return filename.split(".")[:-1]


@click.command()
@click.option(
    "--smoothness-flatfield",
    default=2.5,
    help="Larger value makes the flatfield smoother.",
)
@click.option(
    "--smoothness-darkfield",
    default=5.0,
    help="Larger value makes the darkfield smoother.",
)
@click.option(
    "--sparse-cost-darkfield",
    default=0.01,
    help="Larger value encorages the darkfield sparseness.",
)
@click.option(
    "--max-reweight-iterations",
    default=20,
    help="Maximum number of reweighting iterations.",
)
@click.option(
    "--cpu",
    "device",
    flag_value="cpu",
    help="Use CPU.",
)
@click.option(
    "--gpu",
    "device",
    flag_value="gpu",
    default=True,
    help="Use GPU.",
)
@click.option(
    "--ladmap",
    "fitting_mode",
    flag_value="ladmap",
    default=True,
    help="Use the LADMAP algorithm for fitting.",
)
@click.option(
    "--approximate",
    "fitting_mode",
    flag_value="approximate",
    help="Use the approximate algorithm for fitting.",
)
@click.option("--darkfield", is_flag=True, default=False, help="Calculate darkfields.")
@click.option("--ignore-single-image-error", is_flag=True, default=False, help="Ignore error with the single-sited image.")
@click.argument(
    "input_path",
    required=True,
    type=click.Path(dir_okay=True),
)
@click.argument(
    "output_folder",
    required=True,
    type=click.Path(file_okay=False),
)
def main(
    smoothness_flatfield,
    smoothness_darkfield,
    sparse_cost_darkfield,
    max_reweight_iterations,
    fitting_mode,
    darkfield,
    input_path,
    output_folder,
    device,
    ignore_single_image_error,
):
    if device == "cpu":
        jax.config.update("jax_platform_name", "cpu")
    basic = BaSiC(
        smoothness_flatfield=smoothness_flatfield,
        smoothness_darkfield=smoothness_darkfield,
        sparse_cost_darkfield=sparse_cost_darkfield,
        max_reweight_iterations=max_reweight_iterations,
        fitting_mode=fitting_mode,
        get_darkfield=darkfield,
    )

    flatfields = []
    darkfields = []

    if input_path.is_file():
        logger.info(f"opening images at {input_path}")
        image = AICSImage(input_path)
        for channel in range(image.dims.C):
            images_data = []
            for scene in image.scenes:
                image.set_scene(scene)
                images_data.append(image.get_image_data("MTZYX", C=channel))
            images_data = np.array(images_data).reshape([-1, *images_data[0].shape[-2:]])
            if images_data.shape[0] < 2 and not ignore_single_image_error:
                raise RuntimeError("The image is single sited. Was it saved in the correct way?")
            basic.fit(images_data)
            flatfields.append(basic.flatfield)
            darkfields.append(basic.darkfield)
    else:
        images_data = None
        channels = None
        for image_path in input_path.iterdir():
            image = AICSImage(image_path)
            if channels is None:
                channels = image.channel_names
                images_data = [[] for _ in len(channels)]
            else:
                assert channels == image.channel_names
        for channel in range(len(channels)):
            images_data = []
            for image_path in input_path.iterdir():
                image = AICSImage(image_path)
                for scene in image.scenes:
                    image.set_scene(scene)
                    images_data.append(image.get_image_data("MTZYX", C=channel))
            images_data = np.array(images_data).reshape([-1, *images_data[0].shape[-2:]])
            if images_data.shape[0] < 2 and not ignore_single_image_error:
                raise RuntimeError("The image is single sited. Was it saved in the correct way?")
            basic.fit(images_data)
            flatfields.append(basic.flatfield)
            darkfields.append(basic.darkfield)
    
    output_folder = Path(output_folder)
    input_path2 = get_main_name(input_path)
    flatfield_path = output_folder / (input_path2 + "-ffp.tiff")
    darkfield_path = output_folder / (input_path2 + "-dfp.tiff")
    flatfields = np.moveaxis(np.array(flatfields), 0, -1)
    darkfields = np.moveaxis(np.array(darkfields), 0, -1)
    imsave(flatfield_path, flatfields, check_contrast=False)
    imsave(darkfield_path, darkfields, check_contrast=False)


if __name__ == "__main__":
    main()
