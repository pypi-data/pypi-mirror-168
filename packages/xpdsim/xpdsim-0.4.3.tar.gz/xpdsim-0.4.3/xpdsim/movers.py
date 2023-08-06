from ophyd import Component
from ophyd.sim import Device, SynAxis, SynSignal

cs700 = SynAxis(name="cs700", value=300.0)
cs700.readback.name = "temperature"
shctl1 = SynAxis(name="shctl1", value=0)
shctl1.readback.name = "rad"


class SimFilterBank(Device):
    """Simulated filter bank with only the first filter in by default"""

    flt1 = Component(SynSignal, func=lambda: "In")
    flt2 = Component(SynSignal, func=lambda: "Out")
    flt3 = Component(SynSignal, func=lambda: "Out")
    flt4 = Component(SynSignal, func=lambda: "Out")


fb = SimFilterBank(name="fb")
