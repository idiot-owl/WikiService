from app import db

# A class representing the row of the table in our database
class WikiService(db.Model):
    # Three columns: ID, URL and Fields
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True)
    fields = db.Column(db.Text)

