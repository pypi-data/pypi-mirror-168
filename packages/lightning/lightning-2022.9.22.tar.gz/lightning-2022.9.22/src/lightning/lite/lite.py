try:
    from lightning_lite.lite import LightningLite  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==0.0.0dev`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
