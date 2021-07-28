import threading


def __log(message):
    return f"{threading.current_thread().getName()} | {message}"


def info(message: str):
    print(f"INFO  | {__log(message)}")


def error(message: str):
    print(f"ERROR  | {__log(message)}")


def warn(message: str):
    print(f"WARN  | {__log(message)}")
