import os
from functools import reduce

from imagededup.methods import PHash, AHash, DHash, WHash
import osxmetadata


class Hasher:
  HASHER_LIST = [PHash, AHash, DHash, WHash]
  HASHERS = { h.__name__.lower(): h() for h in HASHER_LIST }


  def __init__(self):
    self.hashers = self.__class__.HASHERS


  def encode_images(self, photos):
    for photo in photos:
      for name, hasher in self.hashers.items():
        photo.hashes[name] = self.__calculate_hash(hasher, photo)


  def encode_video(self, videos):
    # TODO process video poritons of live photos
    # https://stackoverflow.com/questions/9896644/getting-ffprobe-information-with-python
    pass


  def find_duplicates(self, photos):
    return { n: self.__find_duplicates_with_hasher(n, h, photos) for n, h in self.hashers.items() }


  # HELPERS


  def __calculate_hash(self, hasher, photo):
    # TODO take into account photo edits/modifications/live
    return hasher.encode_image(image_file=photo.abspath())


  def __find_duplicates_with_hasher(self, hasher_name, hasher, photos):
    encoding_map = { photo.abspath(): photo.hashes[hasher_name] for photo in photos }
    duplicates = hasher.find_duplicates(encoding_map=encoding_map, scores=True)
    return duplicates
