from flask import request, jsonify
from . import app

@app.route('/')
def home():
  return """
<html>
    <head><title{title}</title></head>
    <body><h1>{title}</h1>
        <p>
            At some point I will make this browsable or playable.
            Until then, it'll just be a simple worker.
        </p>
    </body>
</html>
    """.format(title="HAHAHHAA")

def launch():
  app.run(debug=True, use_reloader=True)
