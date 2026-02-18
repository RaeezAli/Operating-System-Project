import yaml
import os
import logging
from typing import Any

logger = logging.getLogger("Config-Loader")

class ConfigLoader:
    """
    Manages loading and saving configuration for the OS simulator.
    Uses YAML format for readability and structured settings.
    """

    DEFAULT_CONFIG = {
        "scheduler": {
            "default_scheduler": "FCFSScheduler",
            "quantum": 2,
            "context_switch_time": 1
        },
        "memory": {
            "total_memory": 262144,  # 256 KB
            "frame_size": 4096       # 4 KB
        }
    }

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initializes the ConfigLoader.
        
        Args:
            config_path: Path to the YAML configuration file.
        """
        self.config_path = config_path
        self.settings = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> None:
        """
        Loads settings from the YAML file.
        If the file doesn't exist, it creates it with default values.
        """
        if not os.path.exists(self.config_path):
            logger.warning(f"Config file {self.config_path} not found. Creating default...")
            self.save()
            return

        try:
            with open(self.config_path, 'r') as f:
                loaded_settings = yaml.safe_load(f)
                if loaded_settings:
                    # Merge loaded settings with defaults to ensure all keys exist
                    self._deep_merge(self.settings, loaded_settings)
                    logger.info(f"Configuration loaded from {self.config_path}")
                else:
                    logger.warning(f"Config file {self.config_path} is empty. Using defaults.")
        except Exception as e:
            logger.error(f"Failed to load config from {self.config_path}: {e}. Using defaults.")

    def save(self) -> None:
        """Saves current settings to the YAML file."""
        try:
            # Ensure directory exists if path is not in current dir
            dir_name = os.path.dirname(self.config_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
                
            with open(self.config_path, 'w') as f:
                yaml.dump(self.settings, f, default_flow_style=False)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save config to {self.config_path}: {e}")

    def get_config(self) -> dict:
        """Returns the full configuration dictionary."""
        return self.settings

    def get_value(self, section: str, key: str, default: Any = None) -> Any:
        """
        Retrieves a specific value from the configuration.
        
        Args:
            section: The top-level category (e.g., 'scheduler').
            key: The setting name (e.g., 'quantum').
            default: Value to return if key/section is missing.
        """
        try:
            return self.settings.get(section, {}).get(key, default)
        except AttributeError:
            return default

    def _deep_merge(self, base: dict, overlay: dict) -> None:
        """Recursively merges two dictionaries."""
        for key, value in overlay.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

from typing import Any # Added for get_value signature
