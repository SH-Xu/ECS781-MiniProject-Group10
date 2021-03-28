import json

from flask import jsonify
from flask import Flask, request
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from mongoDB import MongoDB

app = Flask(__name__)

@app.route("/")
def index():
    return "This is project work for ECS781 group 10"

@app.route("/search/<isbn>")
def search_book(index):
    pass


@app.route("/mylibrary", methods=["GET"])
def get_books():
    data = request.json
    if data is None or data == {}:
        return Response(
            response=json.dumps({"Error": "Please provide connection information"}),
            status=400,
            mimetype="application/json"
        )
    new_obj = MongoDB(data)
    response = new_obj.read()
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype="application/json"
    )


@app.route("/mylibrary", methods=["POST"])
def add_book():
    data = request.json
    if data is None or data == {} or "Document" not in data:
        return Response(
            response=json.dumps({"Error": "Please provide connection information"}),
            status=400,
            mimetype="application/json"
        )
    new_obj = MongoDB(data)
    response = new_obj.write(data)
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype="application/json"
    )

@app.route("/mylibrary", methods=["PUT"])
def update_book():
    data = request.json
    if data is None or data == {} or "DataToBeUpdated" not in data:
        return Response(
            response=json.dumps({"Error": "Please provide connection information"}),
            status=400,
            mimetype="application/json"
        )
    new_obj = MongoDB(data)
    response = new_obj.update()
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype="application/json"
    )


@app.route("/mylibrary", methods=["DELETE"])
def del_book():
    data = request.json    
    if data is None or data == {}:
        return Response(
            response=json.dumps({"Error": "Please provide connection information"}),
            status=400,
            mimetype="application/json"
        )
    new_obj = MongoDB(data)
    response = new_obj.delete(data)
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
