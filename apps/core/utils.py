from io import BytesIO

from PIL import Image
from django.core.files.storage import default_storage


def create_jpg_thumbnail(image_name: str, target_name: str, size: tuple):
    # If height is higher we resize vertically, if not we resize horizontally
    with Image.open(default_storage.open(image_name, 'rb')) as img:
        # Get current and desired ratio for the images
        img_ratio = img.size[0] / float(img.size[1])
        ratio = size[0] / float(size[1])

        #The image is scaled/cropped vertically or horizontally depending on the ratio
        if ratio > img_ratio:
            img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))), Image.ANTIALIAS)

            box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0], int(round((img.size[1] + size[1]) / 2)))
            img = img.crop(box)

        elif ratio < img_ratio:
            img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]), Image.ANTIALIAS)
            box = (int(round((img.size[0] - size[0]) / 2)), 0, int(round((img.size[0] + size[0]) / 2)), img.size[1])
            img = img.crop(box)
        else:
            img = img.resize((size[0], size[1]), Image.ANTIALIAS)

        # If the scale is the same, we do not need to crop
        image_buffer = BytesIO()
        img.save(image_buffer, 'JPEG')

        image_file = default_storage.open(target_name, 'wb')
        image_file.write(image_buffer.getvalue())
        image_file.flush()
        image_file.close()

        return target_name
