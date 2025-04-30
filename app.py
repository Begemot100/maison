import os

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
# port = int(os.environ.get("PORT", 8000))



app.config['SESSION_COOKIE_SECURE'] = True      # Только через HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True    # Недоступна из JS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'   # Защита от CSRF


LANGUAGES = ['en', 'ru', 'es']

@app.after_request
def disable_etag(response):
    response.headers.pop('ETag', None)
    return response


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
    session.permanent = True

    form = BookingForm()
    df = pd.read_excel('static/data/fin33.xlsx')
    services = {}
    for idx, row in df.iterrows():
        category = row['Категория']
        service = row['Название']
        price = row['Цена ']
        services.setdefault(category, []).append({'service': service, 'price': price})

    # ⬇️ Перемести вот эти блоки сюда, вне цикла
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

        "Masaje Gua Sha 45 min": _("Gua Sha Massage 45 min"),
        "Masaje Gua Sha 30 min": _("Gua Sha Massage 30 min"),
        "Masaje espalda 45": _("Back massage 45 min"),
        "Masaje facial 60 min": _("Facial massage 60 min"),
        "Masaje facial 45 min": _("Facial massage 45 min"),
        "Masaje facial 30 min": _("Facial massage 30 min"),
        "Fisioterapia": _("Physiotherapy"),
        "Masaje corporal": _("Full body massage"),
        "Masaje deportivo": _("Sports massage"),
        "Masaje de espalda": _("Back massage"),
        "Presoterapia": _("Pressotherapy"),
        "Masaje con ventosas": _("Cupping massage"),
        "Masaje relajante": _("Relaxing massage"),
        "Masaje clásico": _("Classic massage"),
        "Masaje facial modelador": _("Facial sculpting massage"),
        "45 Masaje anticelulítico": _("45-min Anti-cellulite massage"),
        "Pedicura completa sin esmalte": _("Full pedicure without polish"),
        "Pedicura completa con esmalte semipermanente": _("Full pedicure with semi-permanent polish"),
        "Quitar esmalte semipermanente": _("Remove semi-permanent polish"),
        "Diseño Frances": _("French design"),

        "Manicura con esmalte normal niñas 12 años": _("Manicure with regular polish for girls (up to 12 years)"),
        "Pedicura completa masculina": _("Men's full pedicure"),
        "ParafinoTerapia para pies": _("Paraffin therapy for feet"),
        "ParafinoTerapia para manos": _("Paraffin therapy for hands"),
        "Manicura japonesa sin esmalte": _("Japanese manicure without polish"),

        "Extensiones de uñas talla XL sin manicura": _("XL size nail extensions without manicure"),
        "Extensiones de uñas talla L sin manicura": _("L size nail extensions without manicure"),
        "Extensiones de uñas talla M sin manicura": _("M size nail extensions without manicure"),
        "Extensiones de uñas talla S sin manicura": _("S size nail extensions without manicure"),

        "Quitar uñas de gel": _("Remove gel nails"),
        "Estampado en todas las uñas": _("Stamp design on all nails"),
        "Extension rellenar 1 uña": _("Refill 1 nail extension"),
        "Diseño en una uña": _("Design on one nail"),
        "Diseño en todas las uña": _("Design on all nails"),
        "Manicura completa con esmalte normal": _("Full manicure with regular polish"),
        "Manicura completa sin esmalte": _("Full manicure without polish"),
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
            "photo": "images_webp/teams_webp/tolio.webp",
            "description": _("Hello! I'm Tolio, a hair stylist with experience in Europe's top international salons. My mission is to help people feel confident and stylish every day. I specialize in crafting looks that highlight each client's individuality, character, and inner strength. I've been working in the beauty industry since 2004!\n\nWhat I do:\n- Modern haircuts for men and women.\n- Complex color treatments: from natural to bold shades using trendy techniques.\n- Styling for special occasions and daily looks.\n- Hair care and restoration using top professional brands.\n- Personalized style, shape, and color recommendations.\n\nWhy clients choose me:\n- I work with soul and attention to detail.\n- I constantly learn new trends and techniques.\n- I listen deeply and deliver exactly what my clients envision.\n- I use only high-quality, professional products.\n\nIf you want more than just a haircut — if you want style — I’m the one. Let's create your perfect new look together!")
        },

        {
            "id": 2,
            "name": "Andrew",
            "position": "TOP COLORIST",
            "photo": "images_webp/teams_webp/andrew.webp",
            "description": _("I’m Andrew — a professional master colorist and educator with over 11 years of experience in the beauty industry. My goal is to create a personalized look that fits you perfectly, makes you feel confident, and stays modern and relevant.\n\nServices I offer:\n• Hair coloring (Blonde, AirTouch, HandTouch, Balayage, California highlights, Shatush, Teasing)\n• Hair toning\n• Hair restoration after coloring (masks, styling, treatments)\n• Consultations to choose a new style and look\n• Women's haircuts and styling\n\nEducation and Courses:\n• 1 year basic training at S&A Group\n• Advanced education: Erteqoob, Hair Sekta, Yulia Litvinova, Esicov\n\nWork Approach:\n• Worked with Ukrainian TV channel STB and singer Nadya Dorofeeva\n• My focus is on highlighting your strengths through the right cut and color\n• I create styles that reflect your individuality and fit your lifestyle\n\nWork Experience:\n• Master Colorist at Art Space Ar4i Stail salon, Kyiv (2014–2023)\n• Specialized in complex techniques (AirTouch, Balayage, Shatush, Teasing)\n• Hair toning and professional care\n• Training and mentoring junior stylists\n• Women's cuts and styling of any complexity")
        },

        {
            "id": 3,
            "name": "Olga",
            "position": "STYLIST",
            "photo": "images_webp/teams_webp/olga.webp",
            "description": _("My name is Olga — I am a professional colorist with over 7 years of experience in the beauty industry. My goal is to create hair color that takes into account the condition, individuality, style, and fashion trends, highlighting your personality. I work only with time-tested and practice-proven materials from top global brands, following the latest trends in coloring. My works are not just coloring, but an artistic approach.\n\nServices I offer:\n• Hair coloring in one tone and various techniques: highlighting, AirTouch, blonde, toning.\n• Hair care and restoration based on knowledge of hair structure and trichology.\n• 'Exit from black' procedures and consultations for color selection.\n\nEducation and Courses:\n• Viart Color Academy — Professional Colorist Course (2018)\n• Hairsekta Color and Styling School\n• Wella education, Estel-Pro\n• Master classes in personalized coloring (2017)\n\nMy approach:\n• Individual approach — I believe that a hairdresser is like a doctor, and every client is a unique case.\n• Following trends — I continually study new techniques and methods in coloring.\n• Hair health care — My colorings are not only beautiful but also safe. I use quality, safe materials and restore hair health with strengthening procedures.\n\nWork experience:\n• PremiumHairBar — Colorist (2017–2022)\n• Professional hair coloring in complex techniques (balayage, ombre, shatush)\n• Hair toning and care\n\nMassage therapist:\n• Massage courses at 'Partner Plus', Kyiv (2016)\n• 'Rehabilitologist School', Bila Tserkva — learning work with musculoskeletal dysfunctions\n• Numerous seminars and workshops\n• Currently studying in Spain as a physiotherapy assistant (auxiliar de fisioterapia)\n\nApproach:\n• Gentle and individual\n• Massage as a space for recovery and trust\n• Constant growth as a specialist")


        },

        {
            "id": 4,
            "name": "Ruzanna",
            "position": "TOP MANICURE MASTER",
            "photo": "images_webp/teams_webp/ruz.webp",
            "description": _("I am a professional nail technician with almost 20 years of experience. I work with various techniques (combination, machine, classic) and improve my qualifications every year, believing that there is always something new to learn and new heights to reach! I love beauty, which is why I chose this profession. I consider myself organized, punctual, and meticulous.")
        },

        {
            "id": 5,
            "name": "Julia",
            "position": "TOP MANICURE MASTER",
            "photo": "images_webp/teams_webp/jul.webp",
            "description": _("Hi! My name is Julia, and I’ve been working as a manicure master for 9 years  Over this time, I’ve not only gained experience — I’ve turned my work into real art   I master various techniques: combined, machine, and classic — I always choose what suits you best   I do both manicures and pedicures and confidently handle even the most difficult corrections   I work quickly  and neatly because I know my craft!  I create any kind of nail designs — from minimalism to full creativity   My mission is to make stunning nails so you leave with a smile, feeling like your hands are true works of art   I’m a warm, open, and positive person   I love my job and treat it with soul and full responsibility   Come visit — we’ll chat, laugh, and of course, make something beautiful!   I’m a nail artist with over 9 years of experience. I love drawing and creating unique, creative designs. Speed and quality are my specialties. Watercolor is my personal passion — I love playing with colors!")
        },

        {
            "id": 6,
            "name": "Ivanna",
            "position": "TOP MANICURE MASTER",
            "photo": "images/iv.webp",
            "description": _("My name is Ivanna, and for the past 7 years I have been creating beauty and confidence at the fingertips of my clients. Once, I simply admired beautiful nails on Instagram and dreamed of having my own look just as well-groomed and stylish. Back then, I had no idea that one day I would become a master who could give this feeling to others. My journey began with curiosity. I bought a lamp, tools, gel polishes, and started practicing on myself and my friends. There were mistakes, nerves, and shaky hands, but with each new manicure I fell more deeply in love with this craft. I trained with the best, attended courses, studied materials and techniques, and constantly improved. Today, I am proud to offer my clients: • Classic, combined, and machine manicures • Nail extensions • Unique designs • Hand and skin care For me, a manicure is not just a job. It's creativity, communication, and an atmosphere of comfort and care. My clients come not only for beautiful nails but also for emotions, trust, and the feeling of being truly cared for. And my story is just beginning.")

        },
        {
            "id": 7,
            "name": "Anna",
            "position": "MASSAGE THERAPIST",
            "photo": "images_webp/teams_webp/anna.webp",
            "description": "Top Manicure Masters",
        },

        {
            "id": 8,
            "name": "Konstantin",
            "position": "MASSAGE THERAPIST",
            "photo": "images/Kost.webp",
            "description": "Top Manicure Masters",
        },
        {
            "id": 9,
            "name": "Oxana",
            "position": "MAKEUP ARTIST",
            "photo": "images_webp/teams_webp/Ox.webp",
            "description": "Top Manicure Masters",
        },
        {
            "id": 10,
            "name": "Alexandra",
            "position": "ADMINISTRATOR",
            "photo": "images_webp/teams_webp/alex.webp",
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

@app.after_request
def add_security_headers(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self';"

    return response


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))

    app.run(host="0.0.0.0", port=port, debug=True)
