import sys
import os

import osxphotos

from photo import Photo
from hasher import Hasher

PHOTO_LIBRARY = "/Users/josh/Pictures/Android.photoslibrary"
PHOTO_DIR = "./photos"

SUPPORTED_IMAGE_FORMATS = set(
  ['JPEG', 'PNG', 'BMP', 'MPO', 'PPM', 'TIFF', 'GIF', 'SVG', 'PGM', 'PBM']
)

def main():
  default_path = PHOTO_LIBRARY
  path = sys.argv[1] if len(sys.argv) > 1 else default_path
  photo_library_path = os.path.expanduser(path)

  photosdb = osxphotos.PhotosDB(photo_library_path)
  photos = [ Photo(p) for p in filter(is_image_supported, photosdb.photos()) ]

  hasher = Hasher()
  encodings = hasher.encode_images(photos)
  duplicates = hasher.find_duplicates(photos)

def is_image_supported(photo):
  file_extension = os.path.splitext(photo.path)[1]
  return file_extension[1:].upper() in SUPPORTED_IMAGE_FORMATS

if __name__ == "__main__":
  main()