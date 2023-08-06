class FailedToExecuteJobException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class FailedToAddJobToQueueException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CompilationException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class JobCancelledError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidStreamMetadataError(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class ConfigValidationException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class ConfigSerializationException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)
