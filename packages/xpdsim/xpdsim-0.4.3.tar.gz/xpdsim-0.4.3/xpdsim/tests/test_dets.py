from pathlib import Path

import bluesky.plan_stubs as bs
import bluesky.plans as bp
import numpy as np
import pytest
from cycler import cycler
from numpy.testing import assert_array_equal
from ophyd import sim
from tifffile import imread
from xpdsim.area_det import (BLACKFLY_IMG_SIZE, DEXELA_IMG_SIZE, PE_IMG_SIZE,
                             XPD_SHUTTER_CONF, add_fake_cam, build_image_cycle,
                             chess_path, det_factory, nsls_ii_path)
from xpdsim.movers import shctl1

test_params = [("nslsii", nsls_ii_path), ("chess", chess_path)]


def get_latest_squeezed_image(db, key: str) -> np.ndarray:
    return db[-1].primary.read()[key].data.squeeze()


@pytest.mark.parametrize(("name", "fp"), test_params)
def test_img_shape(name, fp):
    p = Path(fp)
    shape_check = [imread(str(fp)).shape == PE_IMG_SIZE for fp in p.glob("*.tif*")]
    assert all(shape_check)


def test_add_cam():
    device = sim.SynSignalWithRegistry(name="yolo")
    det = add_fake_cam(device)
    assert hasattr(det, "images_per_set")
    assert hasattr(det, "number_of_sets")
    assert hasattr(det, "cam")
    assert hasattr(det.cam, "acquire_time")
    assert hasattr(det.cam, "acquire")


@pytest.mark.parametrize(("name", "fp"), test_params)
def test_dets(RE, db, fp, name):
    det = det_factory(build_image_cycle(fp))
    RE.subscribe(db.v1.insert, "all")
    uid = RE(bp.count([det]))
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    db_img = get_latest_squeezed_image(db, "pe1_image")
    cycler_img = next(cg)["pe1_image"]
    assert_array_equal(db_img, cycler_img)
    assert db_img.squeeze().shape == PE_IMG_SIZE
    assert cycler_img.squeeze().shape == PE_IMG_SIZE
    assert uid is not None


@pytest.mark.parametrize(("name", "fp"), test_params)
def test_dets_shutter(RE, db, name, fp):
    det = det_factory(cycle=build_image_cycle(fp), shutter=shctl1)
    RE.subscribe(db.v1.insert, "all")
    uid = RE(bp.count([det]))
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    # With the shutter down
    RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["close"], wait=True))
    uid = RE(bp.count([det]))
    img = get_latest_squeezed_image(db, "pe1_image")
    assert_array_equal(img, np.zeros_like(img))
    assert uid is not None
    # With the shutter up
    RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["open"], wait=True))
    print("outside shutter id =", id(shctl1))
    print("outside shutter status =", shctl1.get())
    uid = RE(bp.count([det]))
    img = get_latest_squeezed_image(db, "pe1_image")
    assert_array_equal(img, next(cg)["pe1_image"])
    assert uid is not None


@pytest.mark.parametrize(
    ("shutter", "noise"),
    [(x, y) for x in [None, shctl1] for y in [None, np.random.poisson]],
)
def test_dexela(RE, db, shutter, noise):
    print(DEXELA_IMG_SIZE)
    det = det_factory(
        shutter=shutter, noise=noise, size=DEXELA_IMG_SIZE, data_key="dexela_image"
    )
    RE.subscribe(db.v1.insert, "all")
    RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["open"], wait=True))
    uid = RE(bp.count([det]))
    db_img = get_latest_squeezed_image(db, "dexela_image")
    assert db_img.squeeze().shape == DEXELA_IMG_SIZE
    assert uid is not None
    if shutter:
        RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["close"], wait=True))
        uid = RE(bp.count([det]))
        db_img = get_latest_squeezed_image(db, "dexela_image")
        assert db_img.squeeze().shape == DEXELA_IMG_SIZE
        assert np.allclose(db_img, np.zeros_like(db_img))
        assert uid is not None


@pytest.mark.parametrize(
    ("shutter", "noise"),
    [(x, y) for x in [None, shctl1] for y in [None, np.random.poisson]],
)
def test_blackfly(RE, db, shutter, noise):
    for cycle in [None, cycler("blackfly_det_image", [np.ones(BLACKFLY_IMG_SIZE)])]:
        det = det_factory(
            cycle=cycle,
            data_key="blackfly_det_image",
            shutter=shutter,
            noise=noise,
            size=BLACKFLY_IMG_SIZE,
        )
        RE.subscribe(db.v1.insert, "all")
        RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["open"], wait=True))
        uid = RE(bp.count([det]))
        db_img = get_latest_squeezed_image(db, "blackfly_det_image")
        assert db_img.squeeze().shape == BLACKFLY_IMG_SIZE
        assert uid is not None
        if shutter:
            RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["close"], wait=True))
            uid = RE(bp.count([det]))
            db_img = get_latest_squeezed_image(db, "blackfly_det_image")
            assert db_img.squeeze().shape == BLACKFLY_IMG_SIZE
            assert np.allclose(db_img, np.zeros_like(db_img))
            assert uid is not None
