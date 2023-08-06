import pyFAI
from xpdsim import *

DEVICE_LIST = [
    "simple_pe1c",
    "xpd_pe1c",
    "xpd_pe2c",
    "dexela",
    "blackfly",
    "blackfly_full_field",
    "ring_current",
]


def test_load_pyfai():
    print(pyfai_poni)
    assert pyFAI.load(pyfai_poni)


def test_all_devices():
    assert all([x in globals() for x in DEVICE_LIST])
