from src.shared.errors.main_error import MainError


class InvalidRequest(MainError):
    def __init__(self, message: str):
        super().__init__(f"No request found. {message}")


class MissingParameter(MainError):
    def __init__(self, message: str):
        super().__init__(f"Missing {message} parameter.")
