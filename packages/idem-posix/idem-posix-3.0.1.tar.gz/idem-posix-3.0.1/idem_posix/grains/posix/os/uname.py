import os


async def load_uname(hub):
    (
        hub.grains.GRAINS.kernel,
        hub.grains.GRAINS.nodename,
        hub.grains.GRAINS.kernelrelease,
        hub.grains.GRAINS.kernelversion,
        _,
    ) = os.uname()
