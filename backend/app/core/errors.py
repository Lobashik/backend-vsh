class AppError(Exception):
    """Base application error for API mapping."""


class ConflictError(AppError):
    pass


class NotFoundError(AppError):
    pass


class PermissionDeniedError(AppError):
    pass


class ValidationError(AppError):
    pass
