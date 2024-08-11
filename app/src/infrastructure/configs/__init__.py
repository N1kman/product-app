__all__ = {
    "DBConfig",
}

from .db import DBConfig

from pathlib import Path
from dotenv import load_dotenv

absolute_path = Path("../../_envs").resolve()

for env_file in absolute_path.glob("*.env*"):
    load_dotenv(dotenv_path=env_file)
