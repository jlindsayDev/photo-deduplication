from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object("config")

from app.module_one.controllers import module_one

app.register_blueprint(module_one)


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)



# class Library(db.Model):
#     id = Column(Integer, primary_key=True)
#     type = Column(Enum(LibraryType), nullable=False)
#     name = Column(String, nullable=False)
#     path = Column(String, nullable=False)

# class Photo(db.Model):
#     id = Column(BigIntegerType, primary_key=True)
#     library_id = Column(Integer, ForeignKey(Library.id), nullable=False)
#     path = Column(String, nullable=False)
#     uuid = Column(String, nullable=False)

