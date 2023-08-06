try:
    from lightning_app.frontend.panel.panel_frontend import _logger  # noqa: F401
    from lightning_app.frontend.panel.panel_frontend import has_panel_autoreload  # noqa: F401
    from lightning_app.frontend.panel.panel_frontend import PanelFrontend  # noqa: F401
    from lightning_app.frontend.panel.panel_frontend import _get_allowed_hosts  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_app import __version__
    msg = f'Your `lightning` package was built for `lightning_app==0.6.2`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
