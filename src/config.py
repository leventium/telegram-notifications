import os
import pathlib

default_plugins_path = pathlib.Path(__file__).parent.parent.joinpath("plugins")

TOKEN = os.environ["TOKEN"]
PASSWORD = os.getenv("PASSWORD", "")
PLUGINS_PATH = os.getenv("PLUGINS_PATH", str(default_plugins_path))
