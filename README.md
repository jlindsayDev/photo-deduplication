# Photo Library Dedupe

## Photo Deduplication

Deduplicate photos in photo library using [imagededup](https://idealo.github.io/imagededup/) hashing algorithms (PHash, AHash, WHash, DHash) and EXIF data

- [ ] Scan photo directory/library
- [ ] Create hashes of each photo
  - [ ] JPEG, PNG, BMP, GIF formats
  - [ ] HEIC, HEIF formats (will try [pyheif](https://github.com/david-poirier-csn/pyheif))
  - [ ] Google/Android Photos with Motion
  - [ ] Burst Photos
  - [ ] Apple Live Photos
  - [ ] Video
- [ ] Persist photo hashing scores in SQLite db
- [ ] Group photos based on hashing scores
- [ ] Delete duplicates based on hashing values
  - [ ] Allow selection of photos from group

## Photo Manager

Manage photo edits and duplicates in simple UI

- [ ] Simple flask server
- [ ] WebExtensions browser addon
  - [ ] Firefox
  - [ ] Chrome
  - [ ] React or React Native? (Android app)
- [ ] Create photos from Live Photo snapshots
- [ ] Display graph of Photo edits

## Photo Uploader

Reduce iCloud storage usage by replacing iCloud originals with compressed Google Photos copies. Store originals in Amazon Photos (unlimited storage with Amazon Prime).

- [ ] Download photos in batches (with rate limiting options)
  - [ ] Amazon
  - [ ] Google
- [ ] Upload photos in batches (with throttling options)
  - [ ] Amazon
  - [ ] Google
- [ ] Test photo data fidelity (upload original to service, download from service, compare to original)
  - [ ] iCloud
  - [ ] Google Photos
  - [ ] Amazon Photos

### API Reference Docs

- [Google Photos](https://developers.google.com/photos/library/reference/rest)
- [Amazon Photos](https://developer.amazon.com/docs/amazon-drive/ad-restful-api-nodes.html)
