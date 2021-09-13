# Photo Library Deduplication


Create an array of distinct photo fingerprints leveraging [imagededup](https://idealo.github.io/imagededup/) hashing algorithms (PHash, AHash, WHash, DHash), EXIF data, and [metadata](https://github.com/RhetTbull/osxmetadata)

### Setup

```shell
poetry install
poetry run python src/main.py [library_paths]
```

Example
```
poetry run python src/main.py library.photoslibrary ~/Pictures /Volumes/ExternalSSD/Photos
```

### Usage

```shell
usage: main.py [-h] [-d DB_PATH] [-v] [--dry-run] [path ...]

Deduplicate photo albums

positional arguments:
  path                  path to .photoslibrary or photo directory

optional arguments:
  -h, --help            show this help message and exit
  -d DB_PATH, --db_path DB_PATH
                        database file path where results persist (defaults to assets/duplicates.db)
  -v, --verbose         verbose logging
  --dry-run             do not write or encode. list what operations would be performed
```

### Goals

- [x] Scan photo directory, Apple .photoslibrary or photos.db with [osxphotos](https://github.com/RhetTbull/osxphotos)
- [x] Create hashes of each photo
  - [x] JPEG, PNG, BMP, GIF formats
  - [ ] HEIC, HEIF formats (will try [pyheif](https://github.com/david-poirier-csn/pyheif))
  - [ ] Leverage [ImageMagick's identification signature](https://imagemagick.org/script/identify.php)
  - [ ] Google/Android Photos with Motion
  - [ ] Burst Photos
  - [ ] Apple Live Photos
  - [ ] Video
- [x] Log results to JSON
- [x] Persist photo hashing scores in SQLite db
- [ ] Partition and group photos based on hashing scores
- [ ] Create new Apple .photolibrary

### References

- [idealo/imagededup](https://github.com/idealo/imagededup)
- [RhetTbull/osxmetadata](https://github.com/RhetTbull/osxmetadata)
- [JohannesBuchner/imagehash](https://github.com/JohannesBuchner/imagehash)
- [devedge/imagehash](https://github.com/devedge/imagehash)
- [david-poirier-csn/pyheif](https://github.com/david-poirier-csn/pyheif)
