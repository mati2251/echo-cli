from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    sample_rate: int = 16_000
    channels: int = 1
    block_duration: float = 0.03
    threshold: float = 0.1
    silence_duration: float = 1.0
    min_speech_duration: float = 0.2
    pre_roll: float = 0.2
    post_roll: float = 0.6
    max_duration: float = 30.0

    @property
    def block_size(self) -> int:
        return int(self.sample_rate * self.block_duration)


def load_config() -> Config:
    return Config()
