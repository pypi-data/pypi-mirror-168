from enum import Enum


class log_level_enum(Enum):
    Error = 1
    Warning = 2
    normal = 3
    pigeonhole = 4


def log(str, log_level: log_level_enum = log_level_enum.normal):
    print(f"{log_level}:{str}")


def log_error(error_message: str):
    log(error_message, log_level_enum.Error)
    raise Exception(error_message)
