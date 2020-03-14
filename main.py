import sys
import os

from photo import Photo
import osxphotos
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

  photos = collect_photos(photo_library_path)
  duplicates = hash_photos(photos)

def collect_photos(library_path):
  photosdb = osxphotos.PhotosDB(library_path)
  photos = [ Photo(p) for p in filter(is_image_supported, photosdb.photos()) ]
  return photos

def hash_photos(photos):
  hasher = Hasher()
  encodings = hasher.encode_images(photos)
  duplicates = hasher.find_duplicates(photos)
  return duplicates

def is_image_supported(photo):
    file_extension = os.path.splitext(photo.path)[1]
    return file_extension[1:].upper() in SUPPORTED_IMAGE_FORMATS

if __name__ == "__main__":
    main()
