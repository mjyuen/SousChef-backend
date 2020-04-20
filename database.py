from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os
import hashlib
import json

from flask_heroku import Heroku

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

CORS(app)
#postgres://vhhabiabmrdtya:d2d626af16f4894a2a656de2ca8158f4414687b9b84ea08f801c2c07d774c6b8@ec2-54-243-241-62.compute-1.amazonaws.com:5432/d9d1mlh0cjs2lf

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://vhhabiabmrdtya:d2d626af16f4894a2a656de2ca8158f4414687b9b84ea08f801c2c07d774c6b8@ec2-54-243-241-62.compute-1.amazonaws.com:5432/d9d1mlh0cjs2lf"

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/tigernest"
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:p@localhost:5432/souschef"

heroku = Heroku(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

#-----------------------------------------------------------------------------------------------------------------------------------------

class TrickyIngredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    original = db.Column(db.String, unique = False)
    rewritten = db.Column(db.String, unique = False)

    def __init__(self, original, rewritten): 
        self.original = original
        self.rewritten = rewritten

class TrickyIngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'original', 'rewritten')

trickyingredient_schema = TrickyIngredientSchema()
trickyingredients_schema = TrickyIngredientSchema(many = True)
@app.route("/tricky", methods=["POST"])
def tricky_add():
    original = request.json['original']
    rewritten = request.json['rewritten']

    new_trickyingredient = TrickyIngredient(original, rewritten)
    print(new_trickyingredient.original)
    print(new_trickyingredient.rewritten)

    db.session.add(new_trickyingredient)
    db.session.commit()	
    
    #return jsonify({"original": new_trickyingredient.original, "rewritten": new_trickyingredient.rewritten})
    return trickyingredient_schema.jsonify(new_trickyingredient)

db.create_all()
#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=os.environ.get("PORT", 5000))