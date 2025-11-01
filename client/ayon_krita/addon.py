import os
from ayon_core.addon import AYONAddon, IHostAddon

from .version import __version__
from .debug_log import debug_log

KRITA_HOST_DIR = os.path.dirname(os.path.abspath(__file__))

debug_log(f"addon.py loaded - Host dir: {KRITA_HOST_DIR}")
debug_log(f"Version: {__version__}")

class KritaAddon(AYONAddon, IHostAddon):
    name = "krita"
    version = __version__
    host_name = "krita"

    def __init__(self):
        super().__init__()
        debug_log(f"KritaAddon.__init__ called")

    def add_implementation_envs(self, env, _app):
        debug_log(f"add_implementation_envs called")
        debug_log(f"App host_name: {getattr(_app, 'host_name', 'N/A')}")
        debug_log(f"App name: {getattr(_app, 'name', 'N/A')}")
        
        # Add requirements to KRITA_PATH
        startup_path = os.path.join(KRITA_HOST_DIR, "startup")
        debug_log(f"Startup path: {startup_path}")
        
        new_krita_path = [startup_path]

        old_krita_path = env.get("KRITA_PATH") or ""
        debug_log(f"Old KRITA_PATH: {old_krita_path}")
        
        for path in old_krita_path.split(os.pathsep):
            if not path:
                continue

            norm_path = os.path.normpath(path)
            if norm_path not in new_krita_path:
                new_krita_path.append(norm_path)

        # Add & (ampersand), it represents "the standard krita Path contents"
        new_krita_path.append("&")
        env["KRITA_PATH"] = os.pathsep.join(new_krita_path)
        debug_log(f"New KRITA_PATH: {env['KRITA_PATH']}")

    def get_launch_hook_paths(self, app):
        debug_log(f"get_launch_hook_paths called")
        debug_log(f"App host_name: {getattr(app, 'host_name', 'N/A')}")
        debug_log(f"Self host_name: {self.host_name}")
        
        if app.host_name != self.host_name:
            debug_log(f"Host name mismatch - returning empty hooks")
            return []
        
        hooks_path = os.path.join(KRITA_HOST_DIR, "hooks")
        debug_log(f"Host name matches! Returning hooks path: {hooks_path}")
        return [hooks_path]

    def get_workfile_extensions(self):
        debug_log(f"get_workfile_extensions called")
        return [".kra"]