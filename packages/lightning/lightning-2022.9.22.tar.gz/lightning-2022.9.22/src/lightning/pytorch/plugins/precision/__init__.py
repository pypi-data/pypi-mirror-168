try:

    from pytorch_lightning.plugins.precision.apex_amp import ApexMixedPrecisionPlugin
    from pytorch_lightning.plugins.precision.deepspeed import DeepSpeedPrecisionPlugin
    from pytorch_lightning.plugins.precision.double import DoublePrecisionPlugin
    from pytorch_lightning.plugins.precision.fsdp_native_native_amp import FullyShardedNativeNativeMixedPrecisionPlugin
    from pytorch_lightning.plugins.precision.fully_sharded_native_amp import FullyShardedNativeMixedPrecisionPlugin
    from pytorch_lightning.plugins.precision.hpu import HPUPrecisionPlugin
    from pytorch_lightning.plugins.precision.ipu import IPUPrecisionPlugin
    from pytorch_lightning.plugins.precision.mixed import MixedPrecisionPlugin
    from pytorch_lightning.plugins.precision.native_amp import NativeMixedPrecisionPlugin
    from pytorch_lightning.plugins.precision.precision_plugin import PrecisionPlugin
    from pytorch_lightning.plugins.precision.sharded_native_amp import ShardedNativeMixedPrecisionPlugin
    from pytorch_lightning.plugins.precision.tpu import TPUPrecisionPlugin
    from pytorch_lightning.plugins.precision.tpu_bf16 import TPUBf16PrecisionPlugin

    from pytorch_lightning.plugins.precision import __all__  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.7.6`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
