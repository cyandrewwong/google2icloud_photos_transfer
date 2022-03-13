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
        self._target_exif_dict = target_exif
        self._exif_dict = {}

    def _modify_geodata(self) -> None:
        """
        Modify the geotag data
        :return: None
        """
        gps_dict = {}
        #
        # 'GPSLatitude':




    def _modify_main(self) -> None:
        pass


    # ********* MAIN METHOD
    def modify(self) -> None:
        img = Image.open(self._image_filepath)
        self._exif_dict = {
            ExifTags.TAGS[k]: v for k, v in img.getexif().items() if k in ExifTags.TAGS
        }
        self._modify_geodata()
        t = ''
        
