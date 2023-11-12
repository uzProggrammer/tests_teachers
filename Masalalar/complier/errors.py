class MemoryLimitError(Exception):
    pass


class TimeLimitError(TimeoutError):
    pass

class ComplationError(Exception):
    pass

class WrongAnswerError(Exception):
    pass

class ImprotError(Exception):
    pass