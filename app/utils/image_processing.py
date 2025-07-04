from __future__ import annotations

from PIL import Image

__all__ = ["detect_inverted", "correct_inversion"]


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
