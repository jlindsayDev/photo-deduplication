# Photo Library Deduplication

This is a blanket repository for my attempt at deduplicating photos in an iCloud Photos Library.

## Image Fingerprinting

Create an array of distinct photo fingerprints leveraging [imagededup](https://idealo.github.io/imagededup/) hashing algorithms (PHash, AHash, WHash, DHash), EXIF data, and [metadata](https://github.com/RhetTbull/osxmetadata)

### Current Dev Status

I off-and-on work on this as a pet-project. Thinking about a live-blog [changelog](changelog.md) for my own reference whenever making any changes.

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

## Photo Manager

Manage photo edits and duplicates in simple UI

- [x] Simple flask server
- [ ] WebExtensions browser addon
  - [ ] Firefox
  - [ ] Chrome
  - [ ] React or React Native? (Android app)
- [ ] [Tauri](https://github.com/tauri-apps/tauri)/Electron "app" (???)
- [ ] Create photos from Live Photo snapshots
- [ ] Display graph of Photo edits
- [ ] Organize photos into albums

## Photo Uploader

Reduce iCloud storage usage by replacing iCloud originals with compressed Google Photos copies. Store originals in Amazon Photos (unlimited storage with Amazon Prime).

- [ ] Download photos in batches (with rate limiting)
  - [ ] Amazon
  - [ ] Google
- [ ] Upload photos in batches (with throttling)
  - [ ] Amazon
  - [ ] Google
- [ ] Test photo data fidelity (upload original to service, download from service, compare to original)
  - [ ] iCloud
  - [ ] Google Photos
  - [ ] Amazon Photos
- [ ] Upsert to photo albums on remote services

### API Reference Docs

- [Google Photos](https://developers.google.com/photos/library/reference/rest)
- [Amazon Photos](https://developer.amazon.com/docs/amazon-drive/ad-restful-api-nodes.html)
  > Important: Amazon Drive has been deprecated! No apps using Amazon Drive can be submitted to the Appstore.
