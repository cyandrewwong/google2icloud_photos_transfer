import logging as log
from typing import Dict, Any
from PIL import Image, ExifTags


class ExifModifier:
    def __init__(self, image_filepath: str, target_exif: Dict[str, Any]):
        """
        :param image_filepath: Filepath of the Image
        :param target_exif: Dictionary containing the target EXIF data to modify TO.
        """
        self._image_filepath = image_filepath
        self._exif_dict = target_exif

    # ********* MAIN METHOD
    def modify(self) -> None:
        img = Image.open(self._image_filepath)
        img_exif = img.getexif()
        if img_exif is None:
            log.debug('No existing EXIF data found.')

        t = ''



