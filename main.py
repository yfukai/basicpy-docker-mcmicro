import logging

import click
import numpy as np
from aicsimageio import AICSImage
from skimage.io import imsave
from pathlib import Path

from basicpy import BaSiC

logger = logging.Logger("basicpy-docker-mcmicro")
logger.setLevel(logging.INFO)

@click.command()
@click.option("--smoothness-flatfield", default=2.5)
@click.option("--smoothness-darkfield", default=1.0)
@click.option("--sparse-cost-darkfield", default=0.01)
@click.option("--ladmap", "fitting_mode", flag_value="ladmap", default=True)
@click.option("--darkfield",is_flag=True,default=False)
@click.option("--approximate", "fitting_mode", flag_value="approximate")
@click.argument("input_path",required=True,type=click.Path(dir_okay=False))
@click.argument("output_folder",required=True,type=click.Path(file_okay=False))
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
        get_darkfield=darkfield
    )
    logger.info(f"opening images at {input_path}")
    image = AICSImage(input_path)

    flatfields = []
    darkfields = []
    for channel in range(image.dims.C):
        images_data=[]
        for scene in image.scenes:
            image.set_scene(scene)
            images_data.append(image.get_image_data("MTZYX",C=channel))
        images_data = np.array(images_data)
        images_data = np.array([images_data[ind] for ind in np.ndindex(images_data.shape[:-2])])
        basic.fit(images_data)
        flatfields.append(basic.flatfield)
        darkfields.append(basic.darkfield)
    output_folder = Path(output_folder)
    flatfield_path = output_folder / (input_path + "-ffp.tiff")
    darkfield_path = output_folder / (input_path + "-dfp.tiff")
    flatfields = np.moveaxis(np.array(flatfields),0,-1)
    darkfields = np.moveaxis(np.array(darkfields),0,-1)
    imsave(flatfield_path, flatfields)
    imsave(darkfield_path, darkfields)

if __name__ == "__main__":
    main()