import requests
import json
from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy

# Creating instances of the web application and setting path of SQLite uri
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# A class representing the row of the table in our database
class WikiService(db.Model):
    # Three columns: ID, URL and Fields
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True)
    fields = db.Column(db.Text)


# Endpoint for deleting the 'fields' column from the table
@app.route('/', methods=['DELETE'])
def delete():
    url_obj_list = WikiService.query.all()
    # Delete all the 'fields' values from the table
    for temp_obj in url_obj_list:
        temp_obj.fields = ''

    db.session.commit()

    # Return Success
    return make_response(jsonify({"message":"Records deleted"}), 200)


# Endpoint for setting the 'fields' column for the given id
@app.route("/", methods=['POST'])
def post():
    data = request.get_json()
    url_id = data['id']
    fields = data['fields']
    
    url_obj = WikiService.query.filter_by(id=url_id).scalar()
    # Checking if the given id is present in the table
    if url_obj:
        url_obj.fields = json.dumps(fields)
        db.session.commit()
        # Return Success
        return make_response(jsonify({"message": "Fields Saved"}), 200)
    else:
        # Return Failure
        return make_response(jsonify({"message": "No entry found for given ID"}), 400)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)