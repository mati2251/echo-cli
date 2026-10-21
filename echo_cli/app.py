from dataclasses import replace

from . import status
from .config import load_config
from .devices import check_devices, device_names
from .errors import EchoError
from .keyboard import PauseKey
from .player import play
from .recorder import record_segment


def run() -> int:
    config = load_config()
    try:
        config = replace(config, sample_rate=check_devices(config))
        print("Echo CLI - press Space to pause, Ctrl+C to quit.")
        status.devices(*device_names(), config.sample_rate)
        with PauseKey() as pause:
            while True:
                if pause.paused:
                    status.paused()
                    pause.wait_until_resumed()
                status.listening()
                audio = record_segment(
                    config,
                    on_speech_start=status.recording,
                    on_level=lambda value: status.level(value, config.threshold),
                    should_stop=lambda: pause.paused,
                )
                if audio is None:
                    continue
                status.playing(len(audio) / config.sample_rate)
                play(audio, config, should_stop=lambda: pause.paused)
    except EchoError as exc:
        status.error(str(exc))
        return 1
    except KeyboardInterrupt:
        print("\nBye!")
        return 0
