import sys
import os
import imagededup
import osxphotos

from imagededup.methods import PHash

PHOTO_LIBRARY = "/Users/josh/Pictures/Android.photoslibrary"
PHOTO_DIR = "./photos"

def flatten_dir(library_path, target_dir="./photos/"):
  # find all photos
  photos = []

  # create symbolic links
  [None for photo in photos

def symbolic_link(photo_path):
  file_name = os.path.basename(photo_file)
  return os.symlink(photo_path, os.path.join(target_dir, file_name))

def main():
  default_path = "/Users/josh/Pictures/Android.photoslibrary"
  photo_library_path = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else default_path)
  
  # Could take a while
  photosdb = osxphotos.PhotosDB(photo_library_path)

  # print(osxphotos.utils.get_last_library_path())
  # print(osxphotos.utils.get_system_library_path())
  # print(photosdb.keywords)

  all_photos = photosdb.photos()

if __name__ == "__main__":
    main()