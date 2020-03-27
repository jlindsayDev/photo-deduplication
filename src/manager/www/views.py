import os
import json

from flask import request, jsonify, Response, url_for
from .. import app

ASSET_DIR = "/Users/josh/Repos/photo-dedupe/src/manager/assets/"
JSON_DIR = os.path.join(ASSET_DIR, "json")
PHOTO_DIR = os.path.join(ASSET_DIR, "photos")

@app.route('/')
def home():
  items = []

  hasher_outfiles = os.listdir(JSON_DIR)
  for filename in hasher_outfiles:
    items.append("<h1>" + filename + "</h1>")

    path = os.path.join(JSON_DIR, filename)
    json_obj = json.load(open(path, "r+"))

    for fn, dupes in json_obj.items():
      if len(dupes) == 0:
        continue
      title = "<h3>{fn}</h3>".format(fn=fn)
      images = [ mk_image_obj(d) for d in dupes ]
      items.append(title + "".join(images))

  body = "".join(items)

  return """<!DOCTYPE html>
<html>
  <head><title>{title}</title></head>
  <body>{body}</body>
</html>
    """.format(title="Photo Dupes", body=body)

def mk_image_obj(dupe):
  src, score = dupe
  filename = src[src.find("originals"):]
  url = url_for("static", filename=filename)
  return "<p><a href=\"{url}\"><img src=\"{url}\" width=\"400px\" /></a><span>{score}</span></p>".format(src=src, score=score, url=url)

def launch(args):
  app.run(debug=True, use_reloader=True)
