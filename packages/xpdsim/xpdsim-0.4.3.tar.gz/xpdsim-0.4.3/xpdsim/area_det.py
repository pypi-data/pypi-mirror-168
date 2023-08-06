""" Spoof detectors """
##############################################################################
#
# xpdsim            by Billinge Group
#                   Simon J. L. Billinge sb2896@columbia.edu
#                   (c) 2016 trustees of Columbia University in the City of
#                        New York.
#                   All rights reserved
#
# File coded by:    Christopher J. Wright, Timothy Liu
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

from pathlib import Path
from tempfile import mkdtemp

import numpy as np
from cycler import cycler
from ophyd import Device, sim
from pkg_resources import resource_filename as rs_fn
from tifffile import imread

# extra config
XPD_SHUTTER_CONF = {"open": 60, "close": 0}
DATA_DIR_STEM = "xpdsim.data"
# image size
PE_IMG_SIZE = (2048, 2048)
DEXELA_IMG_SIZE = (3072, 3088)
BLACKFLY_IMG_SIZE = (20, 24)
# package filepath
nsls_ii_path = rs_fn(DATA_DIR_STEM + ".XPD", "ni")
xpd_wavelength = 0.1823
chess_path = rs_fn(DATA_DIR_STEM, "chess")


def build_image_cycle(path, key="pe1_image"):
    """Build image cycles, essentially generators with endless images

    Parameters
    ----------
    path: str
        Path to the files to be used as the base for the cycle.
    key: str, optional
        key of the entire image sequence. Default to ``'pe1_image'``.

    Returns
    -------
    Cycler:
        The iterable like object to cycle through the images
    """
    p = Path(path)
    imgs = [imread(str(fp)) for fp in p.glob("*.tif*")]
    return cycler(key, imgs)


class SimulatedCam(Device):
    acquire_time = sim.SynSignal(name="acquire_time")
    acquire = sim.SynSignal(name="acquire")


def add_fake_cam(det):
    """Adding simulated cam device signals to the detector

    Parameters
    ----------
    det: SimulatedPE1C instance
        The detector

    Returns
    -------
    det: SimulatedPE1C instance
        The detector
    """
    # plug-ins
    det.images_per_set = sim.SynSignal(name="images_per_set")
    det.number_of_sets = sim.SynSignal(name="number_of_sets")
    det.cam = SimulatedCam(name="cam")
    # set default values
    det.cam.acquire_time.put(0.1)
    det.cam.acquire.put(1)
    det.images_per_set.put(1)
    return det


def img_gen(cycle=None, size=PE_IMG_SIZE, shutter=None, noise=None):
    """Generator of diffraction images from 2D detector.

    The output images is determined by ``cycle`` argument.

    Parameters
    ----------
    cycle: cycler.Cycler, optional
        The iterable like object to cycle through the images.
        Default to images with standard Gaussian noise in
         input size.
    size : tuple, optional
        Tuple to specify image size from the simulated detector.
        Default to ``(2048, 2048)`` (PE detector). Overridden when
        ``cycle`` argument is passed.
    shutter : settable, optional
        Ophyd objects to represent the shutter associated with
         with the detector. If it is not passed, assuming shutter
         is always open. If shutter is passed, assuming it
         follows the same configuration as XPD beamline (60 means open).
    noise : callable, optional
        function to generate noise based on absolute scale of image.
        Default to noise-free.

    Returns
    -------
    img : ndarray
        simulated 2D diffraction image with specified size.
    """
    if cycle is None:
        cycle = cycler(pe1_image=[np.random.random(size)])
    # check data keys
    keys = cycle.keys
    if not len(keys) == 1:
        raise RuntimeError("Only support single data key")
    key = keys.pop()
    gen = cycle()
    next(gen)  # kick-off cycler
    gen = cycle()  # instantiate again
    img = next(gen)[key].copy()
    # if shutter, consider more realistic situation
    if shutter:
        status = shutter.get()
        if np.allclose(status.readback, XPD_SHUTTER_CONF["close"]):
            img = np.zeros(img.shape)
        elif np.allclose(status.readback, XPD_SHUTTER_CONF["open"]):
            if noise:
                img += noise(np.abs(img))
    return img.astype(np.float32)


def det_factory(
    cycle=None, img_gen_func=img_gen, data_key="pe1_image", *args, **kwargs
):
    """Build a simulated detector yielding input image sequence

    Parameters
    ----------
    cycle: cycler.Cycler, optional
        The iterable like object to cycle through the images.
        Default to output images in (2048, 2048) dimension
        with Gaussian(0, 1) noise.
    img_gen_func : callable, optional
        function to return image sequence will be output from
         this detector. The function signature is expected
         to be ``f(cycler, *args, **kwargs)``. Default to
         ``xpdsim.img_gen`` function where simulated shutter
         and noise can be included.
    data_key : str, optional
        data key will be shown in Descriptor. Default to
         ``'pe1_image'``.
    args :
        extra arguments will be passed to
         ``img_gen_func``.
    kwargs :
        extra keyword arguments will be
         passed to ``img_gen_func``.

    Returns
    -------
    det: SimulatedPE1C instance
        The detector

    See also
    --------
    ``xpdsim.img_gen``
    """

    det = sim.SynSignalWithRegistry(
        name=data_key,
        func=lambda: img_gen_func(cycle, *args, **kwargs),
        save_path=mkdtemp(prefix="xpdsim"),
    )
    return add_fake_cam(det)
