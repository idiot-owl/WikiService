# WikiService API
## Introduction
WikiService API is an easy to use Python3 wrapper. It supports extracting type, title, links, thumbnails, etc form the provided Wikipedia Page.
## Getting Started
1. The dependencies used can be found in requirements.txt and can be installed using the following command: <br>
   `pip3 install -r requirements.txt` <br>
2. After installing all the dependencies run the file app.py to start a local server at localhost. <br>
3. Now head over to the client.py and change the parameters for the basic CRUD operations and run the file to get the result.
## Notes
1. The database initially contains 3 rows correspoding to the following: <br>
   id : 1, url : "https://en.wikipedia.org/api/rest_v1/page/summary/Stack_Overflow", fields : *empty* <br>
   id : 2, url : "https://en.wikipedia.org/api/rest_v1/page/summary/Sachin_Tendulkar", fields : *empty* <br>
   id : 3, url : "https://en.wikipedia.org/api/rest_v1/page/summary/Albert_Einstein", fields : *empty* <br>
2. All the methods require a json object as a parameter. <br>
3. The `POST` method replaces the `fields` column in the database.
4. The `PUT` method updates the `fields` column by adding the `addFields` and removing the `removeFields` from the input parameters. Add action is performed first and then the remove action. <br>
5. The `DELETE` method deletes the stored fields for a given `id`.
6. The `GET` method queries for the fields specified in the `fields` array from the input parameters for the given `id`. 
