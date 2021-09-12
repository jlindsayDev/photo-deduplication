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

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  path = Column(String, nullable=False)
  type = Column(Enum(LibraryType))

  photos = relationship("Photo")


class Photo(Base):
  __tablename__ = 'photo'

  __table_args__ = (
    UniqueConstraint('library_id', 'uuid'),
  )

  id = Column(BigIntegerType, primary_key=True)
  library_id = Column(Integer, ForeignKey('library.id'), nullable=False)
  path = Column(String, nullable=False)
  uuid = Column(String, nullable=False)
  hashes = Column(JSON)

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


class Duplicate(Base):
  __tablename__ = 'duplicate'

  __table_args__ = (
    UniqueConstraint('library_id', 'orig_photo_id', 'dup_photo_id', 'hash_name'),
  )

  id = Column(BigIntegerType, primary_key=True)
  library_id = Column(Integer, ForeignKey('library.id'), nullable=False)
  orig_photo_id = Column(BigInteger, ForeignKey('photo.id'), nullable=False)
  dup_photo_id = Column(BigInteger, ForeignKey('photo.id'), nullable=False)
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
