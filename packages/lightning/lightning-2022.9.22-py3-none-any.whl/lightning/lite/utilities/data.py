try:

    from lightning_lite.utilities.data import _WrapAttrTag  # noqa: F401
    from lightning_lite.utilities.data import has_iterable_dataset  # noqa: F401
    from lightning_lite.utilities.data import has_len  # noqa: F401
    from lightning_lite.utilities.data import _update_dataloader  # noqa: F401
    from lightning_lite.utilities.data import _get_dataloader_init_args_and_kwargs  # noqa: F401
    from lightning_lite.utilities.data import _dataloader_init_kwargs_resolve_sampler  # noqa: F401
    from lightning_lite.utilities.data import _auto_add_worker_init_fn  # noqa: F401
    from lightning_lite.utilities.data import _reinstantiate_wrapped_cls  # noqa: F401
    from lightning_lite.utilities.data import _wrap_init_method  # noqa: F401
    from lightning_lite.utilities.data import _wrap_attr_method  # noqa: F401
    from lightning_lite.utilities.data import _replace_dunder_methods  # noqa: F401
    from lightning_lite.utilities.data import _replace_value_in_saved_args  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==0.0.0dev`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
