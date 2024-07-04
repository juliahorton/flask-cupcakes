"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests
from models import db, connect_db, Cupcake
from keys import SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)

def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }


@app.route('/')
def show_home_page():

    return render_template("index.html")


@app.route('/api/cupcakes')
def list_cupcakes():
    """Get data about all cupcakes. Respond with JSON in the following format: 
    {
        "cupcakes": [
            {
            "flavor": "cherry",
            "id": 1,
            "image": "https://tinyurl.com/demo-cupcake",
            "rating": 5.0,
            "size": "large"
            }
        ]
    }
    """

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Get data about a single cupcake. Respond with JSON in the following format: 
    {
        "cupcake": {
            "flavor": "cherry",
            "id": 1,
            "image": "https://tinyurl.com/demo-cupcake",
            "rating": 5.0,
            "size": "large"
        }
    }
    """

    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create a cupcake. Respond with JSON in the following format: 
    {
        "cupcake": {
            "flavor": "cherry",
            "id": 1,
            "image": "https://tinyurl.com/demo-cupcake",
            "rating": 5.0,
            "size": "large"
        }
    }
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    # Return w/ status code 201
    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Update a cupcake. Respond with JSON of updated cupcake in the following format:
    {
        "cupcake": {
            "flavor": "cherry",
            "id": 1,
            "image": "https://tinyurl.com/demo-cupcake",
            "rating": 5.0,
            "size": "large"
        }
    }
    """

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")