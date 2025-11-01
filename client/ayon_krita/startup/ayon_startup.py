# -*- coding: utf-8 -*-
"""AYON Krita startup script - standalone test file."""

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
debug_log("ayon_startup.py executed!")
debug_log("=" * 60)

# Log Python path info
debug_log(f"Python version: {sys.version}")
debug_log(f"Python executable: {sys.executable}")
debug_log(f"Script file: {__file__}")
debug_log(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")

# Log environment variables
debug_log(f"KRITA_PATH: {os.environ.get('KRITA_PATH', 'NOT SET')}")
debug_log(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'NOT SET')}")

# Log sys.path
debug_log(f"sys.path (first 5 entries):")
for i, path in enumerate(sys.path[:5]):
    debug_log(f"  [{i}] {path}")

# Try to import Krita
try:
    debug_log("Attempting to import krita module...")
    from krita import Krita
    app = Krita.instance()
    debug_log(f"Krita app instance: {app}")
    debug_log(f"Active document: {app.activeDocument() if app else 'None'}")
except ImportError as e:
    debug_log(f"Could not import krita: {e}")
except Exception as e:
    debug_log(f"Exception importing krita: {type(e).__name__}: {e}")

# Try to install AYON host integration
try:
    debug_log("Attempting to import ayon_core.pipeline...")
    from ayon_core.pipeline import install_host
    debug_log("Successfully imported install_host")
    
    debug_log("Attempting to import KritaHost...")
    try:
        from ayon_krita.api import KritaHost
        debug_log("Successfully imported KritaHost")
        
        debug_log("Calling install_host(KritaHost())...")
        install_host(KritaHost())
        debug_log("install_host completed successfully!")
    except ImportError as api_error:
        debug_log(f"Could not import KritaHost: {api_error}")
        debug_log("API files may not exist yet - this is OK for debugging")
        debug_log("Plugin addon.py is still being loaded by AYON")
    
except ImportError as e:
    debug_log(f"ImportError: {e}")
    debug_log(f"This might be OK if running outside AYON context")
    debug_log(f"Full sys.path: {sys.path}")
    import traceback
    debug_log(f"Traceback:\n{traceback.format_exc()}")
except Exception as e:
    debug_log(f"Exception during host installation: {type(e).__name__}: {e}")
    import traceback
    debug_log(f"Traceback:\n{traceback.format_exc()}")

debug_log("=" * 60)
debug_log("ayon_startup.py finished")
debug_log("=" * 60)

