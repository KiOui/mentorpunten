import random
import string

from PIL import Image, ImageOps
from io import BytesIO
from django.core.files import File
from pathlib import Path

from django.utils.text import slugify


def convert_image(source, extension, resize_to=None, to_name=None):
    """Convert image to png."""
    image = Image.open(source)
    image = ImageOps.exif_transpose(image)
    if resize_to is not None:
        image.thumbnail(resize_to)
    image = image.convert("RGB")
    image_io = BytesIO()
    image.save(image_io, extension, quality=70)
    if to_name is None:
        image_converted = File(image_io, name=Path(source.name).stem + "." + extension)
    else:
        image_converted = File(image_io, name=to_name)
    return image_converted


def get_random_filename(current_filename):
    """Get a random filename by prefixing a random string."""
    name = slugify(Path(current_filename).stem)
    extension = Path(current_filename).suffix
    allowed_chars = "".join((string.ascii_letters, string.digits))
    unique_id = "".join(random.choice(allowed_chars) for _ in range(16))
    return "{}_{}{}".format(unique_id, name, extension)
