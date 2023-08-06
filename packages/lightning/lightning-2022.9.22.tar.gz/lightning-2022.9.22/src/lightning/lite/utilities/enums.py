try:

    from lightning_lite.utilities.enums import LightningEnum  # noqa: F401
    from lightning_lite.utilities.enums import AMPType  # noqa: F401
    from lightning_lite.utilities.enums import PrecisionType  # noqa: F401
    from lightning_lite.utilities.enums import _StrategyType  # noqa: F401
    from lightning_lite.utilities.enums import _AcceleratorType  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==0.0.0dev`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
