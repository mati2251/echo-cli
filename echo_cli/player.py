import time
from collections.abc import Callable

import numpy as np
import sounddevice as sd

from .config import Config
from .errors import PlaybackError

POLL_INTERVAL = 0.05 


def play(
    audio: np.ndarray,
    config: Config,
    should_stop: Callable[[], bool] = lambda: False,
) -> None:
    try:
        sd.play(audio, samplerate=config.sample_rate)
        end = time.monotonic() + len(audio) / config.sample_rate
        while time.monotonic() < end:
            if should_stop():
                sd.stop()
                return
            time.sleep(POLL_INTERVAL)
        sd.wait()
    except sd.PortAudioError as exc:
        raise PlaybackError(f"Playback failed: {exc}") from exc
