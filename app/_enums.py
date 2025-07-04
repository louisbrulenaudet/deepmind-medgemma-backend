import enum

__all__: list[str] = [
    "ImageMimeTypes",
    "ErrorCodes",
]


class ImageMimeTypes(enum.StrEnum):
    JPEG = "image/jpeg"
    PNG = "image/png"


class ErrorCodes(enum.StrEnum):
    COMPLETION_ERROR = "COMPLETION_ERROR"
    CLIENT_INITIALIZATION_ERROR = "CLIENT_INITIALIZATION_ERROR"
