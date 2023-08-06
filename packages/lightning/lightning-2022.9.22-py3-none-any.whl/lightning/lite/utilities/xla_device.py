try:

    from lightning_lite.utilities.xla_device import TPU_CHECK_TIMEOUT  # noqa: F401
    from lightning_lite.utilities.xla_device import inner_f  # noqa: F401
    from lightning_lite.utilities.xla_device import pl_multi_process  # noqa: F401
    from lightning_lite.utilities.xla_device import XLADeviceUtils  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==0.0.0dev`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
