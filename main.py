#!/usr/bin/env python3
import logging
from pathlib import Path

import click
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
    default=1.0,
    help="Larger value makes the darkfield smoother.",
)
@click.option(
    "--sparse-cost-darkfield",
    default=0.01,
    help="Larger value encorages the darkfield sparseness.",
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
@click.argument(
    "input_path",
    required=True,
    type=click.Path(dir_okay=False),
    help="input OME-TIFF path",
)
@click.argument(
    "output_folder",
    required=True,
    type=click.Path(file_okay=False),
    help="output directory",
)
def main(
    smoothness_flatfield,
    smoothness_darkfield,
    sparse_cost_darkfield,
    fitting_mode,
    darkfield,
    input_path,
    output_folder,
):
    basic = BaSiC(
        smoothness_flatfield=smoothness_flatfield,
        smoothness_darkfield=smoothness_darkfield,
        sparse_cost_darkfield=sparse_cost_darkfield,
        fitting_mode=fitting_mode,
        get_darkfield=darkfield,
    )
    logger.info(f"opening images at {input_path}")
    image = AICSImage(input_path)

    flatfields = []
    darkfields = []
    for channel in range(image.dims.C):
        images_data = []
        for scene in image.scenes:
            image.set_scene(scene)
            images_data.append(image.get_image_data("MTZYX", C=channel))
        images_data = np.array(images_data).reshape([-1, *images_data.shape[-2:]])
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
