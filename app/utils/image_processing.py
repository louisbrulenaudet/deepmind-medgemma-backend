import base64
from PIL import Image

__all__ = ["detect_inverted", "correct_inversion", "pad_base64_string"]


def detect_inverted(image: Image.Image) -> bool:
    """Return True if the image orientation is horizontally flipped."""
    orientation = image.getexif().get(274)
    return orientation == 2


def correct_inversion(image: Image.Image) -> tuple[Image.Image, bool]:
    """Detect and fix inversion in the provided image.

    Args:
        image: Input :class:`PIL.Image.Image`.

    Returns:
        Tuple of the possibly corrected image and a bool indicating if it was
        inverted.
    """
    inverted = detect_inverted(image)
    if inverted:
        return image.transpose(Image.FLIP_LEFT_RIGHT), True
    return image, False


def pad_base64_string(base64_string: str) -> str:
    """
    Pads a base64 string with '=' characters to ensure it has a valid length.
    """
    missing_padding = len(base64_string) % 4
    if missing_padding != 0:
        base64_string += "=" * (4 - missing_padding)
    return base64_string
