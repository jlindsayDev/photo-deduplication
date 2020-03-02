import pyheif

class Photo:
  def __init__(self, photo):
    self.photo = photo
    self.path = photo.path
    self.hashes = {}

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
    return self.__repr__()
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
