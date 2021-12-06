class SupplierException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MissingInfo(SupplierException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class WrongArgType(SupplierException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class OutOfRange(SupplierException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UserDefinedIdError(SupplierException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DuplicateProduct(SupplierException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidFormat(SupplierException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
