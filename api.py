from flask import Flask, request, json
from db.data_layer import DataLayer
import atexit
app = Flask(__name__)

dataLayer = DataLayer()


@app.route("/")
def get():
    pass


@app.route("/person/<int:p_id>")
def get_person(p_id):
    person = dataLayer.get_person_by_id(p_id)
    resp = app.response_class(response={"person", json.dumps(person)}, status=200, mimetype="application/json")
    return resp


@app.route("/person")
def get_persons_by_last_name():
    last_name = request.args.get("last_name")
    persons = dataLayer.get_person_by_last_name(last_name)
    resp = app.response_class(response=json.dumps(persons), status=200, mimetype="application/json")
    return resp


@app.route("/person", methods=["POST"])
def add_person():
    user_content = request.json
    row_count = dataLayer.insert_person(user_content["first_name"], user_content["last_name"], user_content["age"],
                                        user_content["address"])

    resp = app.response_class(response=json.dumps({"added_row": row_count}), status=200, mimetype="application/json")
    return resp


@atexit.register
def goodbye():
    dataLayer.shutdown_db()


if __name__ == "__main__":
    app.run()

