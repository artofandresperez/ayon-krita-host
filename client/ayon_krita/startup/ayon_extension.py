# -*- coding: utf-8 -*-
"""AYON Krita Extension - loads when Krita starts."""

try:
    from krita import Extension, Krita
    KRITA_AVAILABLE = True
except ImportError:
    KRITA_AVAILABLE = False
    Extension = None
    Krita = None


class AyonExtension(Extension):
    """AYON host integration extension for Krita."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    def setup(self):
        """Called when extension is set up."""
        import os
        import sys
        
        # Import debug_log
        try:
            from ayon_krita.debug_log import debug_log
        except ImportError:
            try:
                from ayon_core.lib import Logger
                _logger = Logger.get_logger("ayon_krita")
                def debug_log(msg):
                    _logger.debug(msg)
            except ImportError:
                def debug_log(msg):
                    print(f"[AYON KRITA] {msg}")
        
        debug_log("=" * 60)
        debug_log("AYON Extension setup() called")
        debug_log("=" * 60)
        
        # Add parent directory to sys.path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(os.path.dirname(script_dir))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
            debug_log(f"Added to sys.path: {parent_dir}")
        
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
    
    def createActions(self, window):
        """Create actions for the extension."""
        # Actions can be added here if needed
        pass


# Register the extension when module is loaded
if KRITA_AVAILABLE:
    try:
        app = Krita.instance()
        if app:
            app.addExtension(AyonExtension(app))
    except Exception as e:
        # Log error but don't fail
        try:
            from ayon_krita.debug_log import debug_log
            debug_log(f"Failed to register AyonExtension: {e}")
        except ImportError:
            pass

