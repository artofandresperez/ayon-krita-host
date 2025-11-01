# -*- coding: utf-8 -*-
"""AYON Krita startup script - executed when this module is imported."""

import os
import sys

# Setup debug logging first
try:
    # Add parent directory to sys.path to allow imports
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    parent_parent = os.path.dirname(parent_dir)
    
    if parent_parent not in sys.path:
        sys.path.insert(0, parent_parent)
    
    from ayon_krita.debug_log import debug_log
except ImportError:
    # Fallback if we can't import - try to use AYON Logger directly
    try:
        # Add to sys.path first
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        parent_parent = os.path.dirname(parent_dir)
        if parent_parent not in sys.path:
            sys.path.insert(0, parent_parent)
        
        from ayon_core.lib import Logger
        _logger = Logger.get_logger("ayon_krita")
        def debug_log(msg):
            _logger.debug(msg)
    except ImportError:
        # Last resort - simple print
        def debug_log(msg):
            print(f"[AYON KRITA DEBUG] {msg}")

debug_log("=" * 60)
debug_log("Startup script __init__.py executed!")
debug_log("=" * 60)

# Log Python path info
debug_log(f"Python version: {sys.version}")
debug_log(f"Python executable: {sys.executable}")
debug_log(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
debug_log(f"sys.path: {sys.path[:5]}")

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
    debug_log(f"Full sys.path: {sys.path}")
    import traceback
    debug_log(f"Traceback:\n{traceback.format_exc()}")
except Exception as e:
    debug_log(f"Exception during host installation: {type(e).__name__}: {e}")
    import traceback
    debug_log(f"Traceback:\n{traceback.format_exc()}")

debug_log("=" * 60)

