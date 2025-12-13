from pathlib import Path
import os # give access to functions like reading env variables and working with file system 
import yaml


def _project_root() -> Path :
    """
    1. _project_root() is a function that finds the root folder of your project.
    2.  __file__ → path of this Python file (config_loader.py).
    3. resolve() → makes it an absolute path.
    4. parents[1] → goes two folders up (so if the file is utils/config_loader.py, it returns the project root).
    """
    return Path(__file__).resolve().parents[1]


def load_config (config_path : str | None = None) -> dict : # function to load the YAML file and config_path is the optional path to config file and returns the python dictionary
    # 1: Read the environment variable
    env_path = os.getenv("CONFIG_PATH")

    # 2: Decide which config file to use
    if config_path is None : # If config_path is not given
        config_path = env_path or str(_project_root() / "config" / "config.yaml")

    # 3: Convert to Path
    path = Path(config_path) # converting the string path into Path object for making path handling easier and cross platform

    # 4: Make path absolute (if not already)
    if not path.is_absolute():
        path = _project_root() / path # If the path is relative, combine it with the project root.
        # Ensures Python can find the config file no matter where the code runs from.

    # 5: Check if file exists
    if not path.exists() : 
        raise FileNotFoundError(f"Config file is not found : {path}")
    
    with open (path, 'r' , encoding='utf-8') as f : 
        return yaml.safe_load(f) or {}
    
    """
    1. Opens the YAML file in read mode with UTF-8 encoding.
    2. yaml.safe_load(f) → converts YAML into a Python dictionary.
    3. or {} → if the file is empty, return an empty dictionary instead of None.
    """