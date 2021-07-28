from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)

uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=True)
    coffee_price = db.Column(db.String(250), nullable=True)

class CafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Google Maps URL", validators=[DataRequired(),URL()])
    img_url = StringField("Image URL", validators=[DataRequired(),URL()])
    location = StringField("Cafe Location", validators=[DataRequired()])
    has_sockets = BooleanField('Sockets Available?')
    has_toilet = BooleanField('Toilets Available?')
    has_wifi = BooleanField('Wifi Available?')
    can_take_calls = BooleanField('Call taking Available?')
    seats = StringField('Sockets Available?',validators=[DataRequired()])
    coffee_price = StringField('Sockets Available?',validators=[DataRequired()])
    submit = SubmitField("Submit Post")

db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cafes')
def cafes():
    cafes = db.session.query(Cafe).all()
    return render_template('cafes.html',cafes=cafes)

@app.route('/add_cafe',methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        name = form.name.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        has_sockets = form.has_sockets.data
        has_toilet = form.has_toilet.data
        has_wifi = form.has_wifi.data
        can_take_calls = form.can_take_calls.data
        seats = form.seats.data
        coffee_price = form.coffee_price.data
        new_cafe = Cafe(name=name,map_url=map_url,img_url=img_url,location=location,has_sockets=has_sockets,has_toilet=has_toilet,has_wifi=has_wifi,can_take_calls=can_take_calls,seats=seats,coffee_price=coffee_price)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add_cafe.html',form=form)

@app.route('/delete_cafe/<int:id>',)
def delete(id):
    return render_template('delete.html',id=id)

@app.route('/delete_confirm/<int:id>')
def delete_confirm(id):
    cafe_to_delete = db.session.query(Cafe).get(id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('cafes'))


if __name__ == '__main__':
    app.run(debug=True)