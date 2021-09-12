from functools import reduce
from PIL import Image

from imagededup.methods import PHash, AHash, DHash, WHash
from imagehash import average_hash, phash, dhash, whash, colorhash, crop_resistant_hash, \
                      ImageHash, ImageMultiHash
import osxmetadata


class Hasher:
  IMAGEDEDUP_HASHER_LIST = [PHash, AHash, DHash, WHash]
  IMAGEDEDUP_HASHERS = { h.__name__.lower(): h() for h in IMAGEDEDUP_HASHER_LIST }

  IMAGEHASH_FUNCTION_LIST = [average_hash, phash, dhash, whash, colorhash, crop_resistant_hash]
  IMAGEHASH_FUNCTIONS = { f.__name__.lower(): f for f in IMAGEHASH_FUNCTION_LIST }


  def __init__(self):
    self.hashers = self.__class__.IMAGEDEDUP_HASHERS
    self.hash_funcs = self.__class__.IMAGEHASH_FUNCTIONS


  def encode_images(self, photos):
    for photo in photos:
      for name, hasher in self.hashers.items():
        photo.hashes[name] = self.__imagededup_encode(hasher, photo)

      pil_photo = Image.open(photo.abspath())
      for name, func in self.hash_funcs.items():
        photo.hashes[f"{name}-imagehash"] = self.__imagehash_encode(func, pil_photo)


  def encode_video(self, videos):
    # TODO process video poritons of live photos
    # https://stackoverflow.com/questions/9896644/getting-ffprobe-information-with-python
    pass


  def find_duplicates(self, photos):
    return { n: self.__find_duplicates_with_hasher(n, h, photos) for n, h in self.hashers.items() }


  # HELPERS


  def __imagededup_encode(self, hasher, photo):
    # TODO take into account photo edits/modifications/live
    return hasher.encode_image(image_file=photo.abspath())

  def __imagehash_encode(self, func, photo):
    # TODO do something more with the ImageHash object
    return str(func(photo))

  def __find_duplicates_with_hasher(self, hasher_name, hasher, photos):
    encoding_map = { photo.abspath(): photo.hashes[hasher_name] for photo in photos }
    duplicates = hasher.find_duplicates(encoding_map=encoding_map, scores=True)
    return duplicates
