try:
    import logging

    from lightning_lite.__about__ import *  # noqa: F401, F403
    from lightning_lite.__version__ import version as __version__  # noqa: F401

    from lightning_lite import _root_logger  # noqa: F401
    from lightning_lite import _logger  # noqa: F401

    from lightning_lite.lite import LightningLite  # noqa: E402
    from lightning_lite.utilities.seed import seed_everything  # noqa: E402

    from lightning_lite import __all__  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==0.0.0dev`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
