import sounddevice as sd

from .config import Config
from .errors import DeviceUnavailableError

FALLBACK_SAMPLE_RATES = (48_000, 44_100)

SOUND_SERVER_DEVICES = ("pipewire", "pulse")


def check_devices(config: Config) -> int:
    _prefer_sound_server()
    microphone = _query("input", "microphone")
    speaker = _query("output", "playback device")

    candidates = [
        config.sample_rate,
        int(microphone["default_samplerate"]),
        int(speaker["default_samplerate"]),
        *FALLBACK_SAMPLE_RATES,
    ]
    candidates = list(dict.fromkeys(candidates)) 
    for rate in candidates:
        if _supports(sd.check_input_settings, rate, config) and _supports(
            sd.check_output_settings, rate, config
        ):
            return rate

    tried = ", ".join(f"{rate} Hz" for rate in candidates)
    raise DeviceUnavailableError(
        f"The microphone and playback device have no common sample rate "
        f"with {config.channels} channel(s) (tried {tried})."
    )


def device_names() -> tuple[str, str]:
    return (
        _query("input", "microphone")["name"],
        _query("output", "playback device")["name"],
    )


def _prefer_sound_server() -> None:
    try:
        available = list(sd.query_devices())
    except Exception:
        return
    for name in SOUND_SERVER_DEVICES:
        for index, device in enumerate(available):
            if (
                device["name"] == name
                and device["max_input_channels"] > 0
                and device["max_output_channels"] > 0
            ):
                sd.default.device = (index, index)
                return


def _query(kind: str, label: str) -> dict:
    try:
        return sd.query_devices(kind=kind)
    except Exception as exc:
        raise DeviceUnavailableError(
            f"No {label} found. Connect one or check your system sound settings. ({exc})"
        ) from exc


def _supports(check, rate: int, config: Config) -> bool:
    try:
        check(channels=config.channels, samplerate=rate)
    except Exception:
        return False
    return True
