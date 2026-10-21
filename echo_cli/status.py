METER_WIDTH = 20


def devices(microphone: str, speaker: str, sample_rate: int) -> None:
    print(f"🎤 Microphone: {microphone}")
    print(f"🔈 Speaker:    {speaker}  ({sample_rate} Hz)")


def listening() -> None:
    print("🎧 Listening... start speaking.")


def level(value: float, threshold: float) -> None:
    # The threshold sits in the middle of the bar.
    filled = min(METER_WIDTH, round(value / threshold * METER_WIDTH / 2))
    bar = "#" * filled + "-" * (METER_WIDTH - filled)
    bar = bar[: METER_WIDTH // 2] + "|" + bar[METER_WIDTH // 2 :]
    print(f"\r   level [{bar}] {value:.4f}  (threshold {threshold:.4f})", end="", flush=True)


def recording() -> None:
    print("\n🔴 Recording... (pause to finish)")


def paused() -> None:
    print("\n⏸️  Paused — press Space to resume.")


def playing(seconds: float) -> None:
    print(f"🔊 Playing back {seconds:.1f}s")


def error(message: str) -> None:
    print(f"❌ {message}")
