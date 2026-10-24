class SubLedgerException(Exception):
    """Base exception for SubLedger domain."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundError(SubLedgerException):
    """Raised when a requested entity does not exist."""
    pass


class BusinessRuleViolationError(SubLedgerException):
    """Raised when an operation violates a domain business rule."""
    pass


class DuplicateEntityError(SubLedgerException):
    """Raised when an entity with unique fields already exists."""
    pass
