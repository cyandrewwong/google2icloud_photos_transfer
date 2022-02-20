import os

from config import Config


class Google2ICloudPhotos:
    def __init__(self, dir_google: str, dir_icloud: str):
        self._dir_google: str = dir_google
        self._dir_icloud: str = dir_icloud

        self._all_files = []
        self._files_json = []
        self._files_photos = []

    def _check_extensions(self) -> None:
        """
        Check all the extensions of the files in the folder. Anything not JPG or JSON is flagged
        :return: None
        """
        extensions = set()

        for i in self._all_files:
            ext_idx = i.rfind('.')
            extensions.add(i[ext_idx + 1:].upper())

        # TODO: Output filenames of unsupported files
        unsupported = [x for x in extensions if x not in Config.supported_extensions]
        if len(unsupported) > 0:
            raise Exception(f'Unsupported Extensions: {unsupported}')

    def run(self) -> None:
        self._all_files = [os.path.join(self._dir_google, x) for x in os.listdir(self._dir_google)]
        self._check_extensions()

        self._files_json = [x for x in self._all_files if x.upper().endswith('.json')]
        self._files_photos = [x for x in self._all_files if not x.upper().endswith('.json')]

        t = ''


if __name__ == '__main__':
    google = r'C:\Users\Andrew Desktop\Pictures\google_photos\Takeout\Google Photos\Childhood'
    icloud = ''

    app = Google2ICloudPhotos(dir_google=google,
                              dir_icloud=icloud)
    app.run()
