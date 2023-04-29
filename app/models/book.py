from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    
    def to_dict(self):
        dict = {}
        dict["id"] = self.id
        dict["title"] = self.title
        dict["description"] = self.description
        return dict