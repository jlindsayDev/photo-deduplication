from imagededup.methods import PHash, AHash, DHash, WHash
import pyheif
import os

class Photo:
  def __init__(self, photo):
    self.photo = photo
    self.path = photo.path
    self.hashes = self.calculate_hashes(photo)

  def calculate_hashes(self, photo):
    return {
      'phash': self.calculate_hash(PHash(), photo),
      'ahash': self.calculate_hash(AHash(), photo),
      'dhash': self.calculate_hash(DHash(), photo),
      'whash': self.calculate_hash(WHash(), photo)
    }

  def calculate_hash(self, hasher, photo):
    return hasher.encode_image(image_file=photo.path)

  def __json__(self):
    return self.photo.json()

  def __repr__(self):
    return str({
      'uuid': self.photo.uuid,
      'path': self.photo.path,
      'date': self.photo.date,
      'hashes': self.hashes,
    })
  
  def __str__(self):
    return self.repr()
    # print(
    #   p.uuid,
    #   p.filename,
    #   p.date,
    #   p.description,
    #   p.title,
    #   p.keywords,
    #   p.albums,
    #   p.persons,
    #   p.path,
    #   p.ismissing,
    #   p.hasadjustments,
    # )
