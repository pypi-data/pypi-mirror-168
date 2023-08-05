from pathlib import Path
from dynaconf import Dynaconf

SETTINGS_TOML_PATH = Path(__file__).parent.joinpath("settings.toml")

settings = Dynaconf(settings_files=[SETTINGS_TOML_PATH], environments=True)
