# -*- coding: utf-8 -*-
"""Execute AYON startup script when Krita launches."""

from ayon_applications import PreLaunchHook, LaunchTypes


class ExecuteStartupScript(PreLaunchHook):
    """Set up environment for AYON startup script execution."""

    app_groups = {"krita"}
    launch_types = {LaunchTypes.local}

    def execute(self):
        """Prepare environment for startup script execution."""
        import os
        
        self.log.info("[AYON KRITA DEBUG] ExecuteStartupScript hook called")
        
        # The startup script will be executed by Krita when it loads Python
        # We just need to ensure the environment is set up correctly
        # The KRITA_PATH is already set by add_implementation_envs
        
        startup_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "startup"
        )
        self.log.info(f"[AYON KRITA DEBUG] Startup directory: {startup_dir}")
        
        # Verify startup script exists
        startup_script = os.path.join(startup_dir, "__init__.py")
        if os.path.exists(startup_script):
            self.log.info(f"[AYON KRITA DEBUG] Startup script found: {startup_script}")
        else:
            self.log.warning(f"[AYON KRITA DEBUG] Startup script not found: {startup_script}")
        
        # Log environment variables
        krita_path = self.launch_context.env.get("KRITA_PATH", "")
        pythonpath = self.launch_context.env.get("PYTHONPATH", "")
        self.log.info(f"[AYON KRITA DEBUG] KRITA_PATH: {krita_path}")
        self.log.info(f"[AYON KRITA DEBUG] PYTHONPATH: {pythonpath}")

