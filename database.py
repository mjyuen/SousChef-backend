from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from sqlalchemy import func, select
import os
import hashlib
import json
from recipeparsing import parse
from flask_heroku import Heroku

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

CORS(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] = database_url

heroku = Heroku(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

#-----------------------------------------------------------------------------------------------------------------------------------------

class TrickyIngredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Unicode, unique = False)

    def __init__(self, text): 
        print(text)
        self.text = text

class TrickyIngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'text')

trickyingredient_schema = TrickyIngredientSchema()
trickyingredients_schema = TrickyIngredientSchema(many = True)

@app.route("/tricky", methods=["POST"])
def tricky_add():
    text = request.json['text']

    new_trickyingredient = TrickyIngredient(text)

    db.session.add(new_trickyingredient)
    db.session.commit()	
    
    #return jsonify({"original": new_trickyingredient.original, "rewritten": new_trickyingredient.rewritten})
    return trickyingredient_schema.jsonify(new_trickyingredient)

@app.route("/gettricky", methods=["GET"])
def tricky_get():
    ingredient = TrickyIngredient.query.order_by(func.random()).first()
    print(ingredient)
    return trickyingredient_schema.jsonify(ingredient)

#---------------------------------------------------------------------------------------------------------------------------------------------

class FixedIngredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    original = db.Column(db.Unicode, unique = False)
    rewritten = db.Column(db.Unicode, unique = False)
    attempts = db.Column(db.Integer, primary_key = False)

    def __init__(self, original, rewritten, attempts): 
        self.original = original
        self.rewritten = rewritten
        self.attempts = attempts

class FixedIngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'original', 'rewritten', 'attempts')

fixedingredient_schema = FixedIngredientSchema()
fixedingredients_schema = FixedIngredientSchema(many = True)
@app.route("/fixed", methods=["POST"])
def fixed_add():
    original = request.json['original']
    rewritten = request.json['rewritten']
    attempts = request.json['attempts']

    new_fixedingredient = FixedIngredient(original, rewritten, attempts)
    print(new_fixedingredient.original)
    print(new_fixedingredient.rewritten)
    print(new_fixedingredient.attempts)

    db.session.add(new_fixedingredient)
    db.session.commit()	
    
    #return jsonify({"original": new_trickyingredient.original, "rewritten": new_trickyingredient.rewritten})
    return fixedingredient_schema.jsonify(new_fixedingredient)

#---------------------------------------------------------------------------------------------------------------------------------------------
# Class to add ingredient texts for labelling 

class IngredientText(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Unicode, unique = False)

    def __init__(self, text): 
        self.text = text

class IngredientTextSchema(ma.Schema):
    class Meta:
        fields = ('id', 'text')

ingredienttext_schema = IngredientTextSchema()
ingredienttexts_schema = IngredientTextSchema(many = True)

@app.route("/addtext", methods=["POST"])
def text_add():
    text = request.json['text']

    new_ingredienttext = IngredientText(text)

    db.session.add(new_ingredienttext)
    db.session.commit()	
    
    #return jsonify({"original": new_trickyingredient.original, "rewritten": new_trickyingredient.rewritten})
    return ingredienttext_schema.jsonify(new_ingredienttext)

@app.route("/gettext", methods=["GET"])
def text_get():
    ingredient = IngredientText.query.order_by(func.random()).first()
    print(ingredient)
    return ingredienttext_schema.jsonify(ingredient)

#---------------------------------------------------------------------------------------------------------------------------------------------

class LabeledIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Unicode, unique = False)
    quantity = db.Column(db.Unicode, unique = False)
    unit = db.Column(db.Unicode, unique = False)
    name = db.Column(db.Unicode, unique = False)
    comment = db.Column(db.Unicode, unique = False)

    def __init__(self, text, quantity, unit, name, comment):
        self.text = text
        self.quantity = quantity
        self.unit = unit
        self.name = name
        self.comment = comment

class LabeledIngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'text', 'quantity', 'unit', 'name', 'comment')

labeledingredient_schema = LabeledIngredientSchema()
labeledingredients_schema = LabeledIngredientSchema(many = True)

@app.route("/addlabel", methods=["POST"])
def label_add():
    text = request.json['text']
    quantity = request.json['quantity']
    unit = request.json['unit']
    name = request.json['name']
    comment = request.json['comment']

    new_labeled = LabeledIngredient(text, quantity, unit, name, comment)
    db.session.add(new_labeled)
    db.session.commit()

    return labeledingredient_schema.jsonify(new_labeled)

@app.route("/parsetext", methods=["POST"])
def text_parse():
    lines = request.json['text']
    result = []
    for line in lines:
        print(line)
        result.append(parse(line))

    return jsonify(result)     

db.create_all()
#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=os.environ.get("PORT", 5000))