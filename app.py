import requests
import json
from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils import *

# Creating instances of the web application and setting path of SQLite uri
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

# Endpoint for deleting the 'fields' column from the table
@app.route('/', methods=['DELETE'])
def delete():
    data = request.get_json()
    url_id = data['id']
    url_obj = WikiService.query.filter_by(id=url_id).scalar()

    # Checking if the given ID is present in the table
    if url_obj:
        # Delete all the 'fields' values from the table for the given ID
        url_obj.fields = ''
        db.session.commit()
        # Return Success
        return make_response(jsonify({"message":"Records Deleted"}), 200)
    else:
        # Return Failure
        return make_response(jsonify({"message": "No entry found for given ID"}), 400)


# Endpoint for setting the 'fields' column for the given ID
@app.route("/", methods=['POST'])
def post():
    data = request.get_json()
    url_id = data['id']
    fields = data['fields']

    url_obj = WikiService.query.filter_by(id=url_id).scalar()
    # Checking if the given ID is present in the table
    if url_obj:
        url_obj.fields = json.dumps(fields)
        db.session.commit()
        # Return Success
        return make_response(jsonify({"message": "Fields Saved"}), 200)
    else:
        # Return Failure
        return make_response(jsonify({"message": "No entry found for given ID"}), 400)


# Endpoint for updating the fields column for the given ID
@app.route("/", methods=['PUT'])
def update():
    data = request.get_json()
    url_id = data['id']
    add_fields = data['addFields']
    remove_fields = data['removeFields']
    
    url_obj = WikiService.query.filter_by(id=url_id).scalar()
    # Checking if the given ID is present in the table
    if url_obj:
        # Fetching details of the ID and adding the 'addFields' to the fields column
        url_fields = json.loads(url_obj.fields)
        url_fields += add_fields
        
        # Removing the 'removeFields'
        # A list for maintaining the invalid fields which were asked to remove but not present in the column
        invalid_remove_fields = []
        for field in remove_fields:
            if field in url_fields:
                # Checking if the field can be removed
                url_fields.remove(field)
            else:
                # If not, add it to the invalid list
                invalid_remove_fields.append(field)

        url_fields = list(set(url_fields))
        url_obj.fields = json.dumps(url_fields)
        db.session.commit()

        invalid_remove_fields = ', '.join(invalid_remove_fields)

        # Returning appropriate responses
        if invalid_remove_fields:
            return make_response(jsonify({"message": invalid_remove_fields + " field(s) were not found and thus weren't removed. Successfully Updated."}), 200)
        else:
            return make_response(jsonify({"message": "Successfully Updated"}), 200)

    else:
        # Return Failure
        return make_response(jsonify({"message": "No entry found for given ID"}), 400)


# Endpoint for getting the result of the query
@app.route("/", methods=['GET'])
def get():
    query_data = request.get_json()
    url_id = query_data['id']
    url_obj = WikiService.query.filter_by(id=url_id).scalar()

    # Checking if the given ID is present in the table
    if not url_obj:
        return make_response(jsonify({"message": "No entry found for given ID"}), 400)

    # Getting the details of the given ID and query
    query_url = url_obj.url
    query_fields = query_data['fields']
    url_fields = json.dumps(url_obj.fields)

    data = json.loads((requests.get(query_url)).content)
    # A dictionary for storing the result of the query
    query_solution = {}

    for field in query_fields:
        field = field.strip()
        # If field is not present in the database return error
        if field not in url_fields: 
            return make_response(jsonify({"message": str(field) + " - No such field found."}), 400)
        else:
            # Splitting the field using delemiter '.'
            curr_data = data
            field_split = field.split('.')
            # Iterating over the fields to get the required value
            for curr_field in field_split:
                # Checking if the current field is a link to another json file 
                # and updating the current data to be used for the next field
                json_data = check_if_json(curr_data, curr_field)
                if json_data:
                    curr_data = json_data
                else:
                    # Checking if the query is an index to a list. Example - api_urls.references.reference_list[0]
                    # and updating the current data to be used for the next field
                    list_data = check_if_list(curr_data, curr_field)
                    if list_data:
                        curr_data = list_data
                    else:
                        # Checking if simply the field exists in the json
                        if curr_field in curr_data:
                            curr_data = curr_data[curr_field]
                        else:
                            # Return if no such field exists
                            return make_response(jsonify({"message": str(field) + " - No such field found."}), 400)                

            # Adding the result of the given field to the dictionary
            query_solution[field] = curr_data

    return make_response(jsonify(query_solution), 200)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)