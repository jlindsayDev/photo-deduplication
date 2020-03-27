import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, Table, BigInteger
from sqlalchemy import cast, type_coerce
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.dialects import sqlite


Base = declarative_base()
BigIntegerType = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')


class Library(Base):
  __tablename__ = 'library'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  path = Column(String, nullable=False)

  photos = relationship("Photo")


class Photo(Base):
  __tablename__ = 'photo'

  id = Column(BigIntegerType, primary_key=True)
  library_id = Column(Integer, ForeignKey('library.id'), nullable=False)
  path = Column(String, nullable=False)
  uuid = Column(String, nullable=False)
  hashes = Column(JSON)

  library = relationship('Library', backref="library")

  def __init__(self, photo, library):
    self.library_id = library.id
    self.uuid = photo.uuid
    self.path = photo.path
    self.hashes = {}


class Duplicate(Base):
  __tablename__ = 'duplicate'

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
