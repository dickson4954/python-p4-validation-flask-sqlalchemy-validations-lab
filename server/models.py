from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validates_name(self,key,name):
        if not name:
            raise ValueError('Name cannot be empty.')
        elif Author.query.filter_by(name=name).first():
            raise ValueError('Name must be unique.')
        return name
    @validates("phone_number")
    def validate_number(self,key,value):
        digits = 0
        for i in value:
            if i.isdigit():
                digits+=1
        if digits !=  10:
            raise ValueError("Number must be 10 digits")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("title")
    def validate_title(self,key,value):
        if ("Won't Believe" in value) or ("Secret" in value) or ("Top" in value) or ("Guess" in value):
            return value
        else:
            raise ValueError("Must have clickbait-y title")
    @validates("content")
    def validate_content(self,key,value):
        if len(value)<250:
            raise ValueError("Content must be at least 250 characters")
        return value
    @validates("summary")
    def validate_summary(self, key, value):
        if len(value) == 250:
            return value
        else:
            raise ValueError("Summary must be maximum of 250 characters")
    @validates("category")
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either Fiction or Non-Fiction")
        return value
    


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
