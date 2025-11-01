import os
from ayon_core.addon import AYONAddon, IHostAddon

from .version import __version__

KRITA_HOST_DIR = os.path.dirname(os.path.abspath(__file__))

class KritaAddon(AYONAddon, IHostAddon):
    name = "krita"
    version = __version__
    host_name = "krita"

    def add_implementation_envs(self, env, _app):
        # Add requirements to KRITA_PATH
        startup_path = os.path.join(KRITA_HOST_DIR, "startup")
        new_krita_path = [startup_path]

        old_krita_path = env.get("KRITA_PATH") or ""
        for path in old_krita_path.split(os.pathsep):
            if not path:
                continue

            norm_path = os.path.normpath(path)
            if norm_path not in new_krita_path:
                new_krita_path.append(norm_path)

        # Add & (ampersand), it represents "the standard krita Path contents"
        new_krita_path.append("&")
        env["KRITA_PATH"] = os.pathsep.join(new_krita_path)

    def get_launch_hook_paths(self, app):
        if app.host_name != self.host_name:
            return []
        return [
            os.path.join(KRITA_HOST_DIR, "hooks")
        ]

    def get_workfile_extensions(self):
        return [".kra"]