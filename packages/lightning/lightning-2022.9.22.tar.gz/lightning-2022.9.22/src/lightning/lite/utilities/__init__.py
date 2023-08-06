try:

    from lightning_lite.utilities.apply_func import move_data_to_device  # noqa: F401
    from lightning_lite.utilities.distributed import AllGatherGrad  # noqa: F401
    from lightning_lite.utilities.enums import _AcceleratorType, _StrategyType, AMPType, LightningEnum  # noqa: F401

    from lightning_lite.utilities.imports import (  # noqa: F401
        _HIVEMIND_AVAILABLE,
        _HOROVOD_AVAILABLE,
        _HPU_AVAILABLE,
        _IPU_AVAILABLE,
        _IS_INTERACTIVE,
        _IS_WINDOWS,
        _POPTORCH_AVAILABLE,
        _TORCH_GREATER_EQUAL_1_10,
        _TORCH_GREATER_EQUAL_1_11,
        _TORCH_GREATER_EQUAL_1_12,
        _TPU_AVAILABLE,
        _XLA_AVAILABLE,
    )
    from lightning_lite.utilities.rank_zero import (  # noqa: F401
        rank_zero_deprecation,
        rank_zero_info,
        rank_zero_only,
        rank_zero_warn,
    )

except ImportError as err:

    from os import linesep
    from lightning_lite import __version__
    msg = f'Your `lightning` package was built for `lightning_lite==0.0.0dev`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
