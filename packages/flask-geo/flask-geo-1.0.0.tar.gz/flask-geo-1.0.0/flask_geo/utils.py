from abc import ABC, abstractmethod


class IValidator(ABC):

    _next_validator = None

    def set_next(self, validator) -> None:
        self._next_validator = validator
        return validator

    @abstractmethod
    def is_valid(self) -> bool:
        if self._next_validator:
            self._next_validator.is_valid()
        return True
