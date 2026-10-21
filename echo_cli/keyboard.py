import os
import sys
import termios
import threading
import tty
from typing import Self


class PauseKey:
    def __init__(self) -> None:
        self._running = threading.Event()
        self._running.set()
        self._saved_terminal = None

    @property
    def paused(self) -> bool:
        return not self._running.is_set()

    def toggle(self) -> None:
        if self.paused:
            self._running.set()
        else:
            self._running.clear()

    def wait_until_resumed(self) -> None:
        while not self._running.wait(timeout=0.1):
            pass

    def __enter__(self) -> Self:
        if sys.stdin.isatty():
            fd = sys.stdin.fileno()
            self._saved_terminal = termios.tcgetattr(fd)
            tty.setcbreak(fd)
            threading.Thread(target=self._read_keys, args=(fd,), daemon=True).start()
        return self

    def __exit__(self, *_) -> None:
        if self._saved_terminal is not None:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self._saved_terminal)

    def _read_keys(self, fd: int) -> None:
        while True:
            key = os.read(fd, 1)
            if not key:
                return
            if key == b" ":
                self.toggle()
