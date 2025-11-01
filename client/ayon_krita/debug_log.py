# -*- coding: utf-8 -*-
"""Debug logging utility for AYON Krita integration."""

import logging

_logger = None


def _get_logger():
    """Get or create the AYON logger."""
    global _logger
    
    if _logger is not None:
        return _logger
    
    try:
        from ayon_core.lib import Logger
        _logger = Logger.get_logger("ayon_krita")
        _logger.setLevel(logging.DEBUG)
    except ImportError:
        # Fallback to standard logging if AYON Logger is not available
        _logger = logging.getLogger("ayon_krita")
        _logger.setLevel(logging.DEBUG)
        # Add a console handler if none exists
        if not _logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s')
            )
            _logger.addHandler(handler)
    except Exception:
        # Last resort - use a basic logger
        _logger = logging.getLogger("ayon_krita")
        _logger.setLevel(logging.DEBUG)
    
    return _logger


def debug_log(message):
    """Write a debug message using AYON Logger."""
    try:
        logger = _get_logger()
        logger.debug(f"[AYON KRITA DEBUG] {message}")
    except Exception:
        # Silently fail - we don't want debug logging to break anything
        pass


def get_logger():
    """Get the logger instance."""
    return _get_logger()

