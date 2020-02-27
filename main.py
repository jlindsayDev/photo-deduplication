import sys
import os
import imagededup

from imagededup.methods import PHash, AHash, DHash, WHash

from photo import Photo

import osxmetadata
import osxphotos

PHOTO_LIBRARY = "/Users/josh/Pictures/Android.photoslibrary"
PHOTO_DIR = "./photos"
SUPPORTED_IMAGE_FORMATS = set(
  ['JPEG', 'PNG', 'BMP', 'MPO', 'PPM', 'TIFF', 'GIF', 'SVG', 'PGM', 'PBM']
)

def find_duplicates_with_hash(hash_algo, encoding_map, photos):
  hasher = get_hasher(hash_algo)
  outfile = hash_algo + '.json'
  return hasher.find_duplicates(encoding_map=encoding_map, scores=True, outfile=outfile)

def build_encoding_map(hash_algo, photos):
  return { photo.path: photo.hashes[hash_algo] for photo in photos }

def main():
  default_path = PHOTO_LIBRARY
  path = sys.argv[1] if len(sys.argv) > 1 else default_path
  photo_library_path = os.path.expanduser(path)
  
  photosdb = osxphotos.PhotosDB(photo_library_path)
  all_photos = filter(is_image_supported, photosdb.photos())
  photos = [ Photo(p) for p in all_photos ]
  
  duplicates_by_hash_algo = {}
  for hash_algo in ['phash', 'ahash', 'dhash', 'whash']:
    encoding_map = build_encoding_map(hash_algo, photos)
    dupes = find_duplicates_with_hash(hash_algo, encoding_map, photos)
    duplicates_by_hash_algo[hash_algo] = dupes

  print(duplicates_by_hash_algo['phash'])

def is_image_supported(photo):
    file_extension = os.path.splitext(photo.path)[1]
    return file_extension[1:].upper() in SUPPORTED_IMAGE_FORMATS

def get_hasher(hash_str):
  return {
    'phash': PHash(),
    'ahash': AHash(),
    'dhash': DHash(),
    'whash': WHash()
  }[hash_str]

if __name__ == "__main__":
    main()