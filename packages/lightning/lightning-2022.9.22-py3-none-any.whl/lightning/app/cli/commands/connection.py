try:
    from lightning_app.cli.commands.connection import connect  # noqa: F401
    from lightning_app.cli.commands.connection import disconnect  # noqa: F401
    from lightning_app.cli.commands.connection import _retrieve_connection_to_an_app  # noqa: F401
    from lightning_app.cli.commands.connection import _get_commands_folder  # noqa: F401
    from lightning_app.cli.commands.connection import _resolve_command_path  # noqa: F401
    from lightning_app.cli.commands.connection import _list_app_commands  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_app import __version__
    msg = f'Your `lightning` package was built for `lightning_app==0.6.2`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
