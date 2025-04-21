from flask import Flask, render_template, request, flash, redirect, url_for, g
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_babel import Babel
from flask_babel import gettext as _

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Замените на безопасный ключ
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)

LANGUAGES = ['en', 'ru', 'es']

@babel.localeselector
def get_locale():
    return request.args.get('lang') or 'en'

# Форма для бронирования
class BookingForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    service = SelectField('Service', choices=[
        ('hair', 'Hair Styling'),
        ('nails', 'Nail Art'),
        ('spa', 'Spa Treatments')
    ], validators=[DataRequired()])
    submit = SubmitField('Book Now')

@app.route('/')
def index():
    form = BookingForm()

    team_members = [
        {
            "id": 1,
            "name": "Tolio",
            "position": "TOP STYLIST",
            "photo": "images/teams/tolio.jpg",
            "description": "TOP COLORIST | CREATOR OF DISTINCTIVE SHADES",
        },

        {
            "id": 2,
            "name": "Andrew",
            "position": "TOP COLORIST",
            "photo": "images/teams/andrew.jpg",
            "description": "TOP COLORIST OF COMPLEX TECHNIQUES",
        },

        {
            "id": 3,
            "name": "Olga",
            "position": "STYLIST",
            "photo": "images/teams/olga.jpg",
            "description": "COLORIST OF COMPLEX TECHNIQUES",
        },
        {
            "id": 4,
            "name": "Ruzanna",
            "position": "TOP MANICURE MASTERS",
            "photo": "images/teams/ruz.jpg",
            "description": "Top Manicure Masters",
        },
        {
            "id": 5,
            "name": "Julia",
            "position": "TOP MANICURE MASTERS",
            "photo": "images/teams/jul.jpg",
            "description": "Top Manicure Masters",
        },

        {
            "id": 7,
            "name": "Anna",
            "position": "MASSAGE THERAPIST",
            "photo": "images/teams/anna.jpg",
            "description": "Top Manicure Masters",

        },
        {
            "id": 9,
            "name": "Oxana",
            "position": "MAKEUP ARTIST",
            "photo": "images/teams/Ox.jpg",
            "description": "Top Manicure Masters",

        },

        {
            "id": 10,
            "name": "Alexandra",
            "position": "ADMINISTRATOR",
            "photo": "images/teams/alex.jpg",
            "description": "Top Manicure Masters",

        }
    ]
    return render_template('index.html', form=form, team_members=team_members)

@app.route('/book', methods=['POST'])
def book():
    form = BookingForm()
    if form.validate_on_submit():
        # Здесь можно добавить логику сохранения данных (например, в базу данных)
        flash('Booking submitted successfully! We will contact you soon.', 'success')
        return redirect(url_for('index'))
    else:
        flash('Please fill out all fields correctly.', 'error')
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)