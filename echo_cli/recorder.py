from collections import deque
from collections.abc import Callable

import numpy as np
import sounddevice as sd

from .config import Config
from .errors import RecordingError


def rms(block: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(block))))


def record_segment(
    config: Config,
    on_speech_start: Callable[[], None],
    on_level: Callable[[float], None] = lambda level: None,
    should_stop: Callable[[], bool] = lambda: False,
) -> np.ndarray | None:
    block_size = config.block_size
    pre_roll = deque(maxlen=max(1, int(config.pre_roll / config.block_duration)))
    silence_blocks_limit = max(1, int(config.silence_duration / config.block_duration))
    max_blocks = int(config.max_duration / config.block_duration)

    recorded: list[np.ndarray] = []
    speech_blocks = 0
    silent_blocks = 0

    try:
        with sd.InputStream(
            samplerate=config.sample_rate,
            channels=config.channels,
            blocksize=block_size,
            dtype="float32",
        ) as stream:
            while True:
                if should_stop():
                    return None
                block, _overflowed = stream.read(block_size)
                block = block.copy()
                level = rms(block)
                loud = level >= config.threshold

                if not recorded:
                    on_level(level)
                    pre_roll.append(block)
                    if loud:
                        recorded.extend(pre_roll)
                        speech_blocks = 1
                        on_speech_start()
                    continue

                recorded.append(block)
                if loud:
                    speech_blocks += 1
                    silent_blocks = 0
                else:
                    silent_blocks += 1

                if silent_blocks >= silence_blocks_limit:
                    if speech_blocks * config.block_duration < config.min_speech_duration:
                        recorded.clear()
                        pre_roll.clear()
                        speech_blocks = silent_blocks = 0
                        continue
                    break
                if len(recorded) >= max_blocks:
                    break
    except sd.PortAudioError as exc:
        raise RecordingError(f"Recording failed: {exc}") from exc

    tail_to_keep = max(1, int(config.post_roll / config.block_duration))
    trim = max(0, silent_blocks - tail_to_keep)
    if trim:
        recorded = recorded[:-trim]
    return np.concatenate(recorded)
