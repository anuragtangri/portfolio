from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")

# Database Configuration (SQLite)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///links.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
CORS(app)  # Allow frontend to access API

# Link Model
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Serve Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Serve Blog Page
@app.route("/blog.html")
def blog():
    return render_template("blog.html")

# Get all links (API Endpoint)
@app.route("/links", methods=["GET"])
def get_links():
    links = Link.query.all()
    return jsonify([{"id": link.id, "url": link.url} for link in links])

# Add a new link (API Endpoint)
@app.route("/links", methods=["POST"])
def add_link():
    data = request.json
    if "url" not in data or not data["url"]:
        return jsonify({"error": "Invalid URL"}), 400

    # Check if URL already exists
    existing_link = Link.query.filter_by(url=data["url"]).first()
    if existing_link:
        return jsonify({"error": "URL already exists"}), 400

    new_link = Link(url=data["url"])
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"message": "Link added", "url": new_link.url})

# Remove selected links (API Endpoint)
@app.route("/links", methods=["DELETE"])
def remove_links():
    data = request.json
    if "ids" not in data or not isinstance(data["ids"], list):
        return jsonify({"error": "Invalid request"}), 400

    Link.query.filter(Link.id.in_(data["ids"])).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({"message": "Selected links removed"})

# Run Flask Server
if __name__ == "__main__":
    print("Server started at http://127.0.0.1:8081")
    app.run(debug=True, port=8081)
