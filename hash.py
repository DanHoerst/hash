import hashlib
import os
import sqlite3
from flask import abort, Flask, g, jsonify, request

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "hash.db"),
    USERNAME=os.getenv("DB_USERNAME", "admin"),
    PASSWORD=os.getenv("DB_PASSWORD", "default")
))


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource("schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command("initdb")
def initdb_command():
    """Creates the database tables."""
    init_db()
    print "Initialized the database."


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def save_hash(sha_hash, message):
    """Saves hash and message to the database"""
    db = get_db()
    db.execute("insert into hashes(hash, message) values (?, ?)", [sha_hash, message])
    db.commit()
    print "Hash was saved."


def fetch_hash(q, q_type):
    """Fetches hash and message from the database. Can be queried by q_type of either hash or message"""
    db = get_db()
    query = "select hash, message from hashes where %s = '%s'" % (q_type, q)
    cur = db.execute(query)
    result = cur.fetchall()
    return result


@app.route("/messages", methods=["POST"])
def create_hash():
    """Generates a hash for a given message. Saves it to the db and returns the hash"""
    data = request.get_json()
    to_hash = data["message"]
    results = fetch_hash(to_hash, "message")
    if not results:
        sha_hash = hashlib.sha256(to_hash).hexdigest()
        save_hash(sha_hash, to_hash)
    else:
        sha_hash = results[0][0]
    return jsonify({"digest": sha_hash})


@app.route("/messages/<string:sha_hash>", methods=["GET"])
def check_hash(sha_hash):
    """Returns the message for a given hash if it has been stored in the db. Otherwise, 404s"""
    message = fetch_hash(sha_hash, "hash")
    if message:
        return jsonify({"meesage": message[0][1]})
    else:
        return abort(404)

if __name__ == "__main__":
    site_address = os.getenv("SITE_ADDRESS", "localhost")
    context = ("%s.crt" % site_address, "%s.key" % site_address)
    app.run(host='0.0.0.0', port=443, ssl_context=context, threaded=True)
