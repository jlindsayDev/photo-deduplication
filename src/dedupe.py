import sys
import os
import logging
from argparse import ArgumentParser
from sqlalchemy import or_

import osxphotos

from hasher import Hasher
from db import Library, Photo, Duplicate, fetch_or_initialize_db


SUPPORTED_IMAGE_FORMATS = set(
  ['JPEG', 'PNG', 'BMP', 'MPO', 'PPM', 'TIFF', 'GIF', 'SVG', 'PGM', 'PBM']
)


def parse_args():
  parser = ArgumentParser(description='Deduplicate photo album')

  parser.add_argument('-l', '--library_path',
    required=True,
    type=check_existence("Photo library"),
    action='store',
    default=osxphotos.utils.get_last_library_path(),
    help='photo library path')

  parser.add_argument('-d', '--db_path',
    type=str,
    action='store',
    default="assets/duplicates.db",
    help="database file name")

  parser.add_argument('-v', '--verbose',
    action='store_true',
    help="verbose logging")

  return parser.parse_args()


def check_existence(arg_name):
  def check_name(path):
    abspath = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(abspath):
      logging.error(f"{arg_name} does not exist: {path}")
      exit(55)
    return abspath
  return check_name


def fetch_library(library_path, db):
  library_name = os.path.basename(library_path)

  conditions = or_(Library.path == library_path, Library.name == library_name)
  library = db.query(Library).filter(conditions).first()

  if not library:
    logging.info(f"Creating Library: ${library_name}")
    library = Library(name=library_name, path=library_path)
    db.add(library)
    db.commit()

  return library


def fetch_photos(library):
  photosdb = osxphotos.PhotosDB(library.path)

  images = photosdb.photos(images=True, movies=False)
  videos = [] # photosdb.photos(images=False, movies=True)
  albums = {} # photosdb.albums_as_dict

  photos = [ Photo(p, library) for p in filter(is_image_supported, images) ]
  logging.info(f"Found {len(photos)} photos, {len(videos)} videos, {len(albums)} albums")
  return (photos, videos, albums)


def is_image_supported(photo):
  file_extension = os.path.splitext(photo.path)[1]
  return file_extension[1:].upper() in SUPPORTED_IMAGE_FORMATS


def persist_photos(photos, db):
  conditions = Photo.uuid.in_([p.uuid for p in photos])
  db_photos = { p[0] for p in db.query(Photo.uuid).filter(conditions).all() }

  new_photos = [ p for p in photos if p.uuid not in db_photos ]
  if new_photos:
    logging.info(f"Inserting {len(new_photos)} new photos")
    db.add_all(new_photos)
    db.commit()


def persist_duplicates(library, duplicates, encodings, db):
  logging.info("Persisting duplicates")

  # get fresh photo data from the database
  photos = db.query(Photo).filter(Photo.library_id == library.id).all()
  keyed_photos = { p.path: p for p in photos }
  db_duplicates = []

  for hash_name, photos in duplicates.items():
    for orig_photo_path, photo_duplicates in photos.items():
      for dup_photo_path, score in photo_duplicates:
        dupe = Duplicate(
          library_id=library.id,
          orig_photo_id=keyed_photos[orig_photo_path].id,
          dup_photo_id=keyed_photos[dup_photo_path].id,
          hash_name=hash_name,
          hash_value=keyed_photos[orig_photo_path].hashes[hash_name],
          score=score
        )
        db_duplicates.append(dupe)

  logging.info(f"Inserting {len(db_duplicates)} DUPLICATES")
  db.add_all(db_duplicates)
  db.commit()


def main():
  args = parse_args()
  db_session = fetch_or_initialize_db(args.db_path)
  library = fetch_library(args.library_path, db_session)
  photos, videos, albums = fetch_photos(library)

  hasher = Hasher()
  logging.info("Encoding images")
  encodings = hasher.encode_images(photos)

  logging.info("Deduplicating images")
  duplicates = hasher.find_duplicates(photos)

  persist_photos(photos, db_session)
  persist_duplicates(library, duplicates, encodings, db_session)


if __name__ == "__main__":
  main()
