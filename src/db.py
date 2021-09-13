import os
import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, BigInteger, Enum
from sqlalchemy import cast, type_coerce
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.dialects import sqlite


Base = declarative_base()
BigIntegerType = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')


class LibraryType(enum.Enum):
  directory = 1
  apple_photos = 2


class Library(Base):
  __tablename__ = 'library'

  __table_args__ = (
    UniqueConstraint('type', 'path'),
  )

  id = Column(Integer, primary_key=True)
  type = Column(Enum(LibraryType), nullable=False)
  name = Column(String, nullable=False)
  path = Column(String, nullable=False)


class Photo(Base):
  __tablename__ = 'photo'

  __table_args__ = (
    UniqueConstraint('library_id', 'uuid'),
  )

  id = Column(BigIntegerType, primary_key=True)
  library_id = Column(Integer, ForeignKey(Library.id), nullable=False)
  path = Column(String, nullable=False)
  uuid = Column(String, nullable=False)

  library = relationship('Library', backref="library")

  def __init__(self, photo, library):
    self.library = library
    self.photo = photo

    self.library_id = library.id
    self.uuid = photo.uuid
    self.path = self.relativepath()
    self.hashes = {}

  def relativepath(self):
    comm = len(os.path.commonpath([self.library.path, self.photo.path])) + 1
    return self.photo.path[comm::] if comm else self.path

  def abspath(self):
    return os.path.join(self.library.path, self.path)

  def filename(self):
    return os.path.basename(self.path)


class HashLibrary(enum.Enum):
  imagededup = 1
  imagehash = 2
  personal = 3


class HashAlgoritm(enum.Enum):
  average = ['average', 'ahash', 'average_hash']
  perceptual = ['perceptual', 'phash']
  difference = ['difference', 'dhash']
  wavelet = ['wavelet', 'whash']
  color = ['color', 'colorhash', 'color_hash']
  crop_resistant = ['crop_resistant', 'crop_resistant_hash']

def get_hash_algo(name):
  name_lower = name.lower()
  for _, hash_algo in HashAlgoritm.__members__.items():
    if name_lower in hash_algo.value:
      return hash_algo


class Encoding(Base):
  __tablename__ = 'encoding'

  __table_args__ = (
    UniqueConstraint('photo_id', 'hash_library', 'algorithm'),
  )

  id = Column(BigIntegerType, primary_key=True)
  photo_id = Column(BigIntegerType, ForeignKey(Photo.id), nullable=False)
  hash_library = Column(Enum(HashLibrary), nullable=False)
  algorithm = Column(Enum(HashAlgoritm), nullable=False)
  value = Column(String, nullable=False)


class Duplicate(Base):
  __tablename__ = 'duplicate'

  __table_args__ = (
    UniqueConstraint('library_id', 'orig_photo_id', 'dup_photo_id', 'hash_name'),
  )

  id = Column(BigIntegerType, primary_key=True)
  library_id = Column(Integer, ForeignKey(Library.id), nullable=False)
  orig_photo_id = Column(BigInteger, ForeignKey(Photo.id), nullable=False)
  dup_photo_id = Column(BigInteger, ForeignKey(Photo.id), nullable=False)
  hash_name = Column(String, nullable=False)
  hash_value = Column(String, nullable=False)
  score = Column(Integer, nullable=False)


def create_all_tables(engine):
  return Base.metadata.create_all(engine)


def fetch_or_initialize_db(db_path):
  db_url = "sqlite://"
  if db_path:
    db_url += f"/{db_path}"

  engine = create_engine(db_url)

  if not os.path.exists(db_path):
    create_all_tables(engine)
  elif not os.path.isfile(db_path):
    raise Exception(f"Not a database file: {db_path}")
  # elsif # TODO use python-magic to determine db type

  Session = scoped_session(sessionmaker(bind=engine))
  return Session()
