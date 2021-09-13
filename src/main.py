import os
import logging
from argparse import ArgumentParser
from sqlalchemy import or_

import osxphotos

from hasher import Hasher
from db import \
  LibraryType, Library, Photo, Duplicate, HashLibrary, HashAlgoritm, Encoding, \
  get_hash_algo, fetch_or_initialize_db


DATABASE_DEFAULT_PATH = "assets/duplicates.db"

SUPPORTED_IMAGE_FORMATS = set(
  ['JPEG', 'PNG', 'BMP', 'MPO', 'PPM', 'TIFF', 'GIF', 'SVG', 'PGM', 'PBM']
)


def parse_args():
  parser = ArgumentParser(description='Deduplicate photo albums')

  parser.add_argument('-d', '--db_path',
    type=str,#check_path_existence("database file"),
    action='store',
    default=DATABASE_DEFAULT_PATH,
    help=f"database file path where results persist (defaults to {DATABASE_DEFAULT_PATH})")

  parser.add_argument('paths',
    metavar='path',
    type=check_path_existence('photo library path'),
    nargs='*',
    action='extend',
    help="path to .photoslibrary or photo directory")

  parser.add_argument('-v', '--verbose',
    action='store_true',
    help="verbose logging")

  parser.add_argument('--dry-run',
    action='store_true',
    help="do not write or encode. list what operations would be performed")

  return parser.parse_args()


def check_path_existence(arg_name):
  def check_name(path):
    abspath = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(abspath):
      logging.error(f"{arg_name} does not exist: {path}")
      exit(55)
    return abspath
  return check_name


def fetch_libraries(paths, db):
  # TODO @j000shDotCom separate directories from apple photos
  return [fetch_or_initialize_library(path, db) for path in paths], []


def fetch_or_initialize_library(library_path, db):
  library_name = os.path.basename(library_path)
  conditions = or_(Library.path == library_path, Library.name == library_name)
  library = db.query(Library).filter(conditions).first()

  if not library:
    logging.info(f"Creating Library: ${library_name}")
    library = Library(name=library_name, path=library_path, type=LibraryType.apple_photos)
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
  logging.info(f"INSERTING {len(photos)} NEW PHOTOS")
  db.add_all(photos)
  db.commit()

  # TODO fix the re-insertion of photos
  # conditions = Photo.uuid.in_([p.uuid for p in photos])
  # db_photos = { p[0] for p in db.query(Photo.uuid).filter(conditions).all() }

  # new_photos = [ p for p in photos if p.uuid not in db_photos ]
  # if new_photos:
  #   logging.info(f"INSERTING {len(photos)} NEW PHOTOS")
  #   db.add_all(photos)
  #   db.commit()


def persist_duplicates(library, duplicates, encodings, db):
  logging.info("Persisting duplicates")

  # get fresh photo data from the database
  photos = db.query(Photo).filter_by(library_id=library.id).all()
  dupes = db.query(Duplicate).filter_by(library_id=library.id).all()

  id_photos = { p.id: p for p in photos }
  keyed_photos = { p.abspath(): p for p in photos }

  org = {}
  for d in dupes:
    temp = org[d.hash_name] if d.hash_name in org else {}
    org[d.hash_name] = temp

    op = id_photos[d.orig_photo_id]
    op_path = op.abspath()
    dp = id_photos[d.dup_photo_id]

    temp = org[d.hash_name][op_path] if op_path in org[d.hash_name].keys() else set()
    org[d.hash_name][op_path] = temp

    org[d.hash_name][op_path].add(dp.abspath())

  db_duplicates = []

  for hash_name, photos in duplicates.items():
    for orig_photo_path, photo_duplicates in photos.items():
      existingpaths = org[hash_name][orig_photo_path] if org and org[hash_name] and orig_photo_path in org[hash_name] else set()

      for dup_photo_path, score in photo_duplicates:
        if dup_photo_path in existingpaths:
          continue

        dupe = Duplicate(
          library_id=library.id,
          orig_photo_id=keyed_photos[orig_photo_path].id,
          dup_photo_id=keyed_photos[dup_photo_path].id,
          hash_name=hash_name,
          hash_value=keyed_photos[orig_photo_path].hashes[hash_name],
          score=score
        )
        db_duplicates.append(dupe)

  if db_duplicates:
    logging.info(f"INSERTING {len(db_duplicates)} NEW DUPLICATES")
    db.add_all(db_duplicates)
    db.commit()


def main():
  args = parse_args()

  library_paths = args.paths
  if not library_paths:
    logging.error('no libraries specified')
    last_library_path = osxphotos.utils.get_last_library_path()
    system_library_path = osxphotos.utils.get_system_library_path()

    resp = input(f"use last .photoslibrary ({last_library_path}) [Y/n] ")
    if not resp or resp.lower() == 'y':
      library_paths.append(last_library_path)
    else:
      exit(2)

  db_session = fetch_or_initialize_db(args.db_path)

  applephotos, directories = fetch_libraries(library_paths, db_session)
  photos, videos, albums = fetch_photos(applephotos[0]) # TODO

  # TODO replace these dry-run guards with decorators
  if args.dry_run:
    logging.info('[dry-run] skipping photo persistence')
  else:
    logging.info('Persisting photo data')
    persist_photos(photos, db_session)

  hasher = Hasher()

  if args.dry_run:
    logging.info('[dry-run] skipping image encoding')
  else:
    logging.info("Encoding images with imagededup")
    imagededup_encodings = hasher.imagededup_encode(photos)

    logging.info("Encoding images with imagehash")
    imagehash_encodings = hasher.imagehash_encode(photos)

    logging.info('Persisting photo encodings')
    encodings = []

    for photo in photos:
      photo_id = photo.id

      for hash_name, value in imagededup_encodings[photo_id].items():
        enc = Encoding(photo_id=photo_id, hash_library=HashLibrary.imagededup, \
          algorithm=get_hash_algo(hash_name), value=value)
        encodings.append(enc)

      for hash_name, value in imagehash_encodings[photo_id].items():
        enc = Encoding(photo_id=photo_id, hash_library=HashLibrary.imagehash, \
          algorithm=get_hash_algo(hash_name), value=value)
        encodings.append(enc)

    db_session.add_all(encodings)
    db_session.commit()


  if args.dry_run:
    logging.info('[dry-run] skipping deduplication check and persistence')
  else:
    pass
    # TODO make this smarter AND ASYNC
    # logging.info("Deduplicating images")
    # duplicates = hasher.find_duplicates(photos)
    # persist_duplicates(library, duplicates, encodings, db_session)


if __name__ == "__main__":
  main()
