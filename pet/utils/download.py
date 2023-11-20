import os
from pathlib import Path
import shutil
import urllib.request
import progressbar
import tempfile

class ProgressBar:
    def __init__(self, title: str = ""):
        self.pbar = None
        self.title = title
        # This is used to covert progress bar unity
        # from Byte to Gigabyte
        self.scale = 1e-6

    def __call__(self, block_num, block_size, total_size):
        block_size = round(block_size * self.scale, 2)
        total_size = round(total_size * self.scale, 2)

        if not self.pbar:
            self.pbar = progressbar.ProgressBar(maxval=total_size, prefix=self.title)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


def download_file(file_link, filename):

    # Checks if the file already exists before downloading
    try:
        if not os.path.isfile(filename):
            temp_file = tempfile.NamedTemporaryFile()
            print(temp_file.name)
            title='Downloading language model'
            urllib.request.urlretrieve(file_link, temp_file.name, reporthook=ProgressBar(title=title))
            shutil.move(temp_file.name, filename)
            print("File downloaded successfully.")
        else:
            print("File already exists.")
    finally:
        temp_file.close()
