import sys

try:
    from echo_cli.app import run
except OSError as exc:
    sys.exit(f"❌ Audio system unavailable: {exc}\nInstall PortAudio (e.g. `sudo apt install libportaudio2`).")

if __name__ == "__main__":
    sys.exit(run())
