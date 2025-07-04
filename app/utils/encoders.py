import base64
import io

from PIL import Image

__all__ = ["ImageEncoder"]


class ImageEncoder:
    """
    Utility class for encoding images to base64 format.

    This class provides a method to convert PIL Image objects into base64-encoded strings,
    which can be used in web applications or APIs that require image data in base64 format.

    Example usage:
        ```python
        from PIL import Image
        from app.utils.encoders import ImageEncoder

        img = Image.open("path/to/image.jpg")
        encoder = ImageEncoder()
        b64_string = encoder.encode_image_to_base64(img)
        print(b64_string)
        ```
    """

    @staticmethod
    def encode_image_to_base64(img: Image.Image) -> str:
        """
        Convert a PIL Image to a base64-encoded string.

        Args:
            img (Image.Image): The PIL Image object to encode.

        Returns:
            str: A base64-encoded string representation of the image.
        """
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{b64}"
