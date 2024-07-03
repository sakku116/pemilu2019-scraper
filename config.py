from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv

@dataclass(frozen=True)
class Env:
    EMAIL: str = getenv("EMAIL", "")
    PASSWORD: str = getenv("PASSWORD", "")