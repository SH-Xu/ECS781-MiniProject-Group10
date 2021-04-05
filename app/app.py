import json
import requests
import base64
import random
import time

from flask import Flask, request
from flask.wrappers import Response
from mongoDB import MongoDB

app = Flask(__name__)

users = {
    'YCH': ['123456']
}

Authority_status = 0


def gen_token(uid):
    s1 = ':'.join([uid, str(random.random()), str(time.time() + 72000)])
    print("\ns1:", s1)
    print("type(s1):", type(s1))
    token = base64.b64encode(s1.encode('utf-8'))
    print("\ntoken:", token)
    print("type(token):", type(token))

    users[uid].append(token)
    return token


def verify_token(token):
    _token = base64.b64decode(token)
    print("\n_token:", _token)
    print("type(_token):", type(_token))

    _token1 = _token.decode('utf-8')
    print("\n_token1:", _token1)
    print("type(_token1):", type(_token1))

    t1 = _token1.split(':')[0]
    print("\nt1:", t1)
    print("type(t1):", type(t1))

    get1 = users.get(_token1.split(':')[0])[-1]
    print("\nget1", get1)

    if not users.get(_token1.split(':')[0])[-1] == token:
        return "The token is not correct or matches your uid "
    if float(_token1.split(':')[-1]) >= time.time():
        return 1
    else:
        return "The token has timed out"


@app.route("/index")
def index():
    global Authority_status
    if Authority_status == 1:
        return "This is project work for ECS781 group 10"
    else:
        return "Please login"


@app.route("/apply_token", methods=["POST", "GET"])
def apply_token():
    r1 = request.headers['Authorization'].split(' ')[-1]
    print("r1:", r1)
    print("type(r1):", type(r1))
    r2 = base64.b64decode(r1)
    print("\nr2: ", r2)
    print("type(r2):", type(r2))
    uid, pw = r2.split(b':')
    # print("uid: ", uid)
    # print("pw: ", pw)
    # print("type(uid): ", type(uid))
    uid1 = uid.decode('utf-8')
    pw1 = pw.decode('utf-8')
    print("\nuid1: ", uid1)
    print("pw1: ", pw1)
    print("type(uid1): ", type(uid1))
    print("type(pw1): ", type(pw1))

    get1 = users.get(uid1)
    print(get1)

    get2 = users.get(uid1)[0]
    print(get2)

    if users.get(uid1)[0] == pw1:
        return gen_token(uid1)
    else:
        return 'error'


@app.route("/login", methods=["POST", "GET"])
def login():
    token = request.args.get("token").encode('utf-8')
    if verify_token(token) == 1:
        global Authority_status
        Authority_status = 1
        return "You have login successfully"
    else:
        return 'error'

@app.route("/logout", methods=["POST", "GET"])
def logout():
    global Authority_status
    if  Authority_status == 1:
        Authority_status = 0
        return "You have logout successfully"
    else:
        return 'You have not login'


@app.route("/detail/<type>/<index>")
def detail_book(type, index):
    global Authority_status
    if Authority_status == 1:
        url = "https://openlibrary.org/api/books?bibkeys={}:{}&format=json".format(type, index)
        return requests.get(url).json()
    else:
        return "Please login"

@app.route("/mylibrary", methods=["GET"])
def get_books():
    global Authority_status
    if Authority_status == 1:
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
            mimetype="application/json")
    else:
       return "Please login"



@app.route("/mylibrary", methods=["POST"])
def add_book():
    global Authority_status
    if Authority_status == 1:
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
    else:
       return "Please login"

@app.route("/mylibrary", methods=["PUT"])
def update_book():
    global Authority_status
    if Authority_status == 1:
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
    else:
       return "Please login"

@app.route("/mylibrary", methods=["DELETE"])
def del_book():
    global Authority_status
    if Authority_status == 1:
        data = request.json
        if data is None or data == {} or "Filter" not in data:
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
    else:
       return "Please login"

if __name__ == "__main__":
    app.run(debug=True)
