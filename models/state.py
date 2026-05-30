from enum import StrEnum


class TaskState(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
    TIMED_OUT = "TIMED_OUT"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def from_str(cls, value: str) -> "TaskState":
        try:
            return cls(value)
        except ValueError:
            return cls.UNKNOWN