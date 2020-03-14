from imagededup.methods import PHash, AHash, DHash, WHash
import osxmetadata
from functools import reduce

class Hasher:
  HASHER_LIST = [PHash, AHash, DHash, WHash]
  HASHERS = { h.__name__.lower(): h() for h in HASHER_LIST }

  @classmethod
  def encode_images(cls, photos):
    for photo in photos:
      for name, hasher in cls.HASHERS.items():
        photo.hashes[name] = cls.calculate_hash(hasher, photo)

  @classmethod
  def encode_video(cls, videos):
    # TODO process video poritons of live photos
    # https://stackoverflow.com/questions/9896644/getting-ffprobe-information-with-python
    pass

  @classmethod
  def find_duplicates(cls, photos):
    return { n: cls.find_duplicates_with_hasher(n, h, photos) for n, h in cls.HASHERS.items() }

  @classmethod
  def calculate_hash(cls, hasher, photo):
    # TODO take into account photo edits/modifications/live
    return hasher.encode_image(image_file=photo.path)

  @classmethod
  def find_duplicates_with_hasher(cls, hasher_name, hasher, photos):
    encoding_map = { photo.path: photo.hashes[hasher_name] for photo in photos }
    outfile = 'json/' + hasher_name + '.json'
    duplicates = hasher.find_duplicates(encoding_map=encoding_map, scores=True, outfile=outfile)
    return duplicates

  @classmethod
  def find_duplicates_to_remove(cls, hasher_name, hasher, photos):
    encoding_map = { photo.path: photo.hashes[hasher_name] for photo in photos }
    duplicates = hasher.find_duplicates_to_remove(encoding_map=encoding_map, scores=True)
    return duplicates
