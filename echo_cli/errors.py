class EchoError(Exception):
    pass


class DeviceUnavailableError(EchoError):
    pass


class RecordingError(EchoError):
    pass


class PlaybackError(EchoError):
    pass
