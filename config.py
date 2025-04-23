from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    client_id: str
    client_secret: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env()

    return Config(
        client_id=env("CLIENT_ID"),
        client_secret=env("CLIENT_SECRET"),
    )
