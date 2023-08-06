from xpdsim.movers import cs700, fb, shctl1


def test_cs700():
    # simple test if the object behaves as default
    assert cs700.readback.name == "temperature"
    cs700.set(310)
    assert cs700.readback.get() == 310


def test_shctl1():
    # simple test if the object behaves as default
    assert shctl1.readback.name == "rad"
    shctl1.set(60)
    assert shctl1.readback.get() == 60


def test_filterbank():
    # simple test if the object behaves as default
    in_flts = [x for x in fb.component_names if x.endswith("1")]
    out_flts = [x for x in fb.component_names if x not in in_flts]
    for flt in out_flts:
        assert getattr(fb, flt).get() == "Out"
    for flt in in_flts:
        assert getattr(fb, flt).get() == "In"
