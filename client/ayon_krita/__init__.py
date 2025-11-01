from .debug_log import debug_log

debug_log("__init__.py loaded")

from .version import __version__

debug_log(f"Importing KritaAddon...")

from .addon import KritaAddon, KRITA_HOST_DIR

debug_log(f"KritaAddon imported successfully")

__all__ = (
    "__version__",
    "KritaAddon",
    "KRITA_HOST_DIR",
)
