from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_babel import Babel, _
import pandas as pd
from flask import make_response
from flask import session, jsonify


import openpyxl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)
port = int(os.environ.get("PORT", 8000))

LANGUAGES = ['en', 'ru', 'es']

@babel.localeselector
def get_locale():
    return request.args.get('lang') or 'en'


@app.after_request
def add_header(response):
    response.cache_control.max_age = 31536000  # 1 год
    return response

@app.context_processor
def inject_globals():
    return dict(currentLang=str(get_locale()))

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
    df = pd.read_excel('static/data/s3.xlsx')
    services = {}
    for idx, row in df.iterrows():
        category = row['Категория']
        service = row['Название']
        price = row['Цена от']
        services.setdefault(category, []).append({'service': service, 'price': price})

        translated_gallery = {
            "Manicure": _("Manicure"),
            "Pedicure": _("Pedicure"),
            "Lashes": _("Lashes"),
            "Hair": _("Hair"),
            "Brows": _("Brows"),
            "Clients": _("Clients"),
            "Endosphera": _("Endospheres")
        }

        translated_services = {
            "Primer corte + tratamiento de regalo": _("First haircut + complimentary treatment"),
            "Primera sesión de endoesfera": _("First endospheres session"),
            "Primera manicura con esmaltado permanente": _("First manicure with permanent polish"),
            "Primera sesión de endoesfera": _("First endospheres session"),
            "Primera manicura con esmaltado permanente": _("First manicure with permanent polish")
        }

    translated_categories = {
        "Paquete de bienvenido solo nuevas clientes": _("Welcome package for new clients"),
        "Masaje": _("Massage"),
        "Pedicura": _("Pedicure"),
        "Manicura": _("Manicure"),
        "Cosmetología": _("Cosmetology"),
        "Consulta": _("Consultation"),
        "Pelo": _("Hair"),
        "Maquillaje": _("Makeup"),
        "Depilacion": _("Hair removal"),
        "endospheres": _("Endospheres"),
        "Extensiones de pestañas": _("Eyelash extensions")
    }

    team_members = [
        {
            "id": 1,
            "name": "Tolio",
            "position": "TOP COLORIST | CREATOR OF DISTINCTIVE SHADES",
            "photo": "images/teams/tolio.jpg",
            "description": "Top stylist with international experience."
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

    return render_template('index.html', form=form, team_members=team_members, services=services,
                           translated_categories=translated_categories, translated_services=translated_services, translated_gallery=translated_gallery)

@app.route('/book', methods=['POST'])
def book():
    form = BookingForm()
    if form.validate_on_submit():
        flash(_('Booking submitted successfully! We will contact you soon.'), 'success')
        return redirect(url_for('index'))
    else:
        flash(_('Please fill out all fields correctly.'), 'error')
    return render_template('index.html', form=form)

@app.route('/shop')
def shop():
    products = [
        {
            "id": 1,
            "name": "Hadat Shampoo 250ml",
            "description": _("Nourishing shampoo for daily care"),
            "price": "38€",
            "image": "images/shop/hadat1.png"
        },
        {
            "id": 2,
            "name": "Hadat Mask 500ml",
            "description": _("Deep hydration hair mask"),
            "price": "48€",
            "image": "images/shop/hadat2.png"
        }
    ]
    return render_template('shop.html', products=products)

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product_map = {
        1: {
            "id": 1,
            "name": "Hadat Shampoo 250ml",
            "price": "18€",
            "image": "images/shop/hadat1.jpg"
        },
        2: {
            "id": 2,
            "name": "Hadat Mask 500ml",
            "price": "28€",
            "image": "images/shop/hadat2.jpg"
        }
    }

    product = product_map.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    cart = session.get('cart', [])
    cart.append(product)
    session['cart'] = cart
    return jsonify({'message': 'Added to cart', 'cart': cart})

@app.route('/cart')
def view_cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)


# @app.route('/add-to-cart/<int:product_id>', methods=['POST'])
# def add_to_cart(product_id):
#     cart = session.get('cart', [])
#     cart.append(product_id)
#     session['cart'] = cart
#     flash(_('Product added to cart!'))
#     return redirect(url_for('shop'))

# @app.route('/cart')
# def view_cart():
#     products = [
#         {
#             "id": 1,
#             "name": "Hadat Shampoo 250ml",
#             "price": "18€",
#             "image": "images/shop/hadat1.jpg"
#         },
#         {
#             "id": 2,
#             "name": "Hadat Mask 500ml",
#             "price": "28€",
#             "image": "images/shop/hadat2.jpg"
#         }
#     ]
#     cart = session.get('cart', [])
#     cart_items = [p for p in products if p['id'] in cart]
#     return render_template('cart.html', cart_items=cart_items)
#


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)
