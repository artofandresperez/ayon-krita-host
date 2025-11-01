# -*- coding: utf-8 -*-
"""AYON Krita startup script."""

import os
import sys

# Import debug_log - add parent directory to path if needed
try:
    from ayon_krita.debug_log import debug_log
except ImportError:
    # Fallback if we can't import - try to use AYON Logger directly
    try:
        from ayon_core.lib import Logger
        _logger = Logger.get_logger("ayon_krita")
        def debug_log(msg):
            _logger.debug(msg)
    except ImportError:
        # Last resort - do nothing
        def debug_log(msg):
            pass

debug_log("=" * 60)
debug_log("Startup script __init__.py executed!")
debug_log("=" * 60)

# Log Python path info
debug_log(f"Python version: {sys.version}")
debug_log(f"Python executable: {sys.executable}")
debug_log(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")

# Try to install AYON host integration
try:
    debug_log("Attempting to import ayon_core.pipeline...")
    from ayon_core.pipeline import install_host
    debug_log("Successfully imported install_host")
    
    debug_log("Attempting to import KritaHost...")
    from ayon_krita.api import KritaHost
    debug_log("Successfully imported KritaHost")
    
    debug_log("Calling install_host(KritaHost())...")
    install_host(KritaHost())
    debug_log("install_host completed successfully!")
    
except ImportError as e:
    debug_log(f"ImportError: {e}")
    debug_log(f"sys.path: {sys.path}")
except Exception as e:
    debug_log(f"Exception during host installation: {type(e).__name__}: {e}")
    import traceback
    debug_log(f"Traceback:\n{traceback.format_exc()}")

debug_log("=" * 60)

