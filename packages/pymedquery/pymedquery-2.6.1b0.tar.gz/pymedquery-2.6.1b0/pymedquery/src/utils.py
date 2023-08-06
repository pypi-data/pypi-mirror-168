from config.logger import get_logger

from nibabel.nifti1 import Nifti1Header, Nifti1Image
from nibabel.spatialimages import HeaderDataError
import numpy as np
from typing import Tuple

log = get_logger(__name__)


def convert2nii(img: np.ndarray, affine: np.ndarray = None, zooms: Tuple[float] = None, is_mask: bool = False) -> Nifti1Image:
    """convert2nii is a utility function that wraps a volume/image in a Nifti1Image object.
    The reason why this is added to pyMedQuery is the need to have medical images wrapped in
    nifti classes for subsequent analyses. There are a lot of legacy software that require
    the images to be wrapped in a nifti.

    Parameters
    ----------
    img : np.ndarray
        img is the 3D medical volume
    affine : np.ndarray
        affine is the 2D 4x4 rotation matrix corresponding to the medical volume
    zooms : Tuple[float]
        zooms are dimensions of the voxel, which are x, y, z in the voxel.
    """
    if not is_mask:
        try:
            header = Nifti1Header()
            header.set_data_dtype(img.dtype)
            header.set_data_shape(img.shape)
            header.set_zooms(zooms)

        except (HeaderDataError, ValueError, TypeError):
            log.error('failed setting values to the nifti header with msg:', exc_info=True)
    else:
        header = None

    try:
        nii_img = Nifti1Image(dataobj=img, affine=affine, header=header)
    except (ValueError, TypeError):
        log.error('failed placing the image, affine and header in the Nifti1Image class:', exc_info=True)

    return nii_img
