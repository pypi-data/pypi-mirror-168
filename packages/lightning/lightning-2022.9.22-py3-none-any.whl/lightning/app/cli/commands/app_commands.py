try:
    from lightning_app.cli.commands.app_commands import _run_app_command  # noqa: F401
    from lightning_app.cli.commands.app_commands import _handle_command_without_client  # noqa: F401
    from lightning_app.cli.commands.app_commands import _handle_command_with_client  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_app import __version__
    msg = f'Your `lightning` package was built for `lightning_app==0.6.2`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
