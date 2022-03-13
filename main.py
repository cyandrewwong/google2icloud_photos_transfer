import os
import json
import logging as log
from collections import namedtuple
from config import Config
from exif_modifier import ExifModifier


class Google2ICloudPhotos:
    fpath_row = namedtuple('filepath_map', ['title', 'fpath_img', 'fpath_json'])

    def __init__(self, dir_google: str, dir_icloud: str):
        self._dir_google: str = dir_google
        self._dir_icloud: str = dir_icloud

        self._files_all = []
        self._map_filepaths = {}

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

    def _build_filepath_map(self) -> None:
        """
        Split the filepaths into photos and jsons
        :return: None
        """
        log.info('Mapping filepaths...')

        # Recall we have already checked all the extensions in Config.supported_extensions
        fpaths_img = [x for x in self._files_all if not x.upper().endswith('.JPG')]
        fpaths_json = [x for x in self._files_all if x.upper().endswith('.JSON')]

        if len(fpaths_json) != len(fpaths_img):
            log.warning(f'Number of files mismatch: JSON {len(fpaths_json)}  IMG {len(fpaths_img)}')

        # Iterate json files to map the filenames
        for fpath in fpaths_json:
            fpath_img = fpath.replace('.JSON', '').replace('.json', '')  # Could be better - if more extensions
            title = os.path.basename(fpath_img).replace('.jpg', '').replace('.JPG', '')
            self._map_filepaths[title] = self.fpath_row(title=title, fpath_img=fpath_img, fpath_json=fpath)

        # Check that all the inferred img jpaths exist
        invalid_imgs = []
        for img, row in self._map_filepaths.items():
            if not os.path.exists(row.fpath_img):
                log.warning(f'{row.fpath_img} does not exist!')
                invalid_imgs.append(img)

    def _process_json_file(self, title: str, fpath_row: fpath_row) -> None:
        """
        Load the given json file and look for the given jpg to edit it
        :param fpath_img: json filepath
        :return: None
        """
        log.debug(f'Processing json {title}')
        try:
            with open(fpath_row.fpath_json) as json_data:

                exif_dict = json.loads(json_data.read())

            json_title = f'{exif_dict.get("title")}'

            if json_title.upper().replace('.jpg', '').replace('.JPG', '') != title.upper():
                raise ValueError(f'Title does not match title in EXIF JSON! File: {title} : JSON title {json_title}')

            modifier = ExifModifier(image_filepath=fpath_row.fpath_img, target_exif=exif_dict)
            modifier.modify()

        except Exception as e:
            log.warning(f'Could not process {title} : {e}')

    def run(self) -> None:
        self._files_all = [os.path.join(self._dir_google, x) for x in os.listdir(self._dir_google)]
        self._check_extensions()
        self._build_filepath_map()

        for title, row in self._map_filepaths.items():
            self._process_json_file(title, row)

        t = ''


if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG)

    google = r'C:\Users\Andrew Desktop\Pictures\google_photos\Takeout\Google Photos\Photos from 1970'
    icloud = ''

    app = Google2ICloudPhotos(dir_google=google,
                              dir_icloud=icloud)
    app.run()
