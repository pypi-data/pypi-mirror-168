try:

    from lightning_app.cli.lightning_cli_delete import delete  # noqa: F401
    from lightning_app.cli.lightning_cli_delete import delete_cluster  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_app import __version__
    msg = f'Your `lightning` package was built for `lightning_app==0.6.2`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
