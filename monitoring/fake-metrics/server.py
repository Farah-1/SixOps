from flask import Response
from flask import Flask

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    with open("storage.prom") as f:
        return Response(
            f.read(),
            mimetype="text/plain"
        )

app.run(host="0.0.0.0", port=9101)
