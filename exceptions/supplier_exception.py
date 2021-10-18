class MissingInfo(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class WrongArgType(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class OutOfRange(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UserDefinedIdError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
