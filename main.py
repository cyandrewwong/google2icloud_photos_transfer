import os
import json
import logging as log
from config import Config
from exif_modifier import ExifModifier


class Google2ICloudPhotos:
    def __init__(self, dir_google: str, dir_icloud: str):
        self._dir_google: str = dir_google
        self._dir_icloud: str = dir_icloud

        self._files_all = []
        self._files_photos = []
        self._map_title2json = {}

    def _check_extensions(self) -> None:
        """
        Check all the extensions of the files in the folder. Anything not JPG or JSON is flagged
        :return: None
        """
        log.info('Checking File Extensions...')
        extensions = set()

        for i in self._files_all:
            ext_idx = i.rfind('.')
            extensions.add(i[ext_idx + 1:].upper())

        unsupported = [x for x in extensions if x not in Config.supported_extensions]
        if len(unsupported) > 0:
            raise Exception(f'Unsupported Extensions: {unsupported}')

    def _split_filepaths(self) -> None:
        """
        Split the filepaths into photos and jsons
        :return: None
        """
        log.info('Splitting filepaths...')
        self._files_photos = [x for x in self._files_all if not x.upper().endswith('.JPG')]
        json_files = [x for x in self._files_all if x.upper().endswith('.JSON')]

        for file in json_files:
            filename = os.path.basename(file)
            self._map_title2json[filename] = file


    def _process_json_file(self, filename: str, filepath: str) -> None:
        """
        Load the given json file and look for the given jpg to edit it
        :param filepath: json filepath
        :return: None
        """
        log.debug(f'Processing json {filepath}')
        try:
            with open(filepath) as file:

                exif_dict = json.loads(file.read())

            image_title = f'{exif_dict.get("title")}.json'

            if image_title.upper() != filename.upper():
                raise ValueError(f'Filename does not match title in EXIF JSON! {filename} : {image_title}')

            if image_title in self._map_title2json.keys():
                modifier = ExifModifier(image_filepath=filepath, target_exif=exif_dict)
                modifier.modify()

        except Exception as e:
            log.warn(f'Could not process {filename} : {e}')

    def run(self) -> None:
        self._files_all = [os.path.join(self._dir_google, x) for x in os.listdir(self._dir_google)]
        self._check_extensions()
        self._split_filepaths()

        for filename, filepath in self._map_title2json.items():
            self._process_json_file(filename, filepath)


        t = ''


if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG)


    google = r'C:\Users\Andrew Desktop\Pictures\google_photos\Takeout\Google Photos\Childhood'
    icloud = ''

    app = Google2ICloudPhotos(dir_google=google,
                              dir_icloud=icloud)
    app.run()
