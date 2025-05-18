import os
from typing import Optional, Dict

class ConfigManager:
    """
    Securely loads and manages configuration values and secrets from environment variables or config files.
    All state is instance-based.
    """

    def __init__(self, env_file: Optional[str] = None):
        """
        Args:
            env_file: Optional path to a .env file for config values.
        """
        self.env_file = env_file
        self.config: Dict[str, str] = {}
        if env_file:
            try:
                with open(env_file) as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            self.config[k] = v
            except Exception:
                pass  # Ignore file errors in skeleton
        # Do NOT overlay with environment variables here; handled in get()

    def get(self, key: str) -> str:
        """
        Retrieves a configuration value by key.
        Args:
            key: The configuration key.
        Returns:
            The configuration value.
        Raises:
            KeyError: If the key is not found.
        """
        # First check environment variable, then fallback to file config
        if key in os.environ:
            return os.environ[key]
        if key in self.config:
            return self.config[key]
        raise KeyError(key)