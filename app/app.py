from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')
# admin password can be set via env var ADMIN_PASSWORD; default for dev
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'letmein')

db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(100))
    bookings = db.relationship('Booking', backref='client', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(50), unique=True, nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Do not expose bookings to public visitors. Only show to admins.
    if session.get('is_admin'):
        bookings = Booking.query.order_by(Booking.created_at.desc()).all()
        return render_template('index.html', bookings=bookings, admin=True)
    return render_template('index.html', admin=False)


@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('index.html', bookings=bookings, admin=True)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        pw = request.form.get('password')
        if pw == ADMIN_PASSWORD:
            session['is_admin'] = True
            flash('Logged in as admin', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid password', 'danger')
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Logged out', 'info')
    return redirect(url_for('index'))

@app.route('/deals')
def deals():
    featured = [
        {
            'title': 'Maldives Overwater Retreat',
            'desc': '7 nights in an overwater villa, transfers, and excursions.',
            'image': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80'
        },
        {
            'title': 'Tropical Island Escape',
            'desc': 'Beachfront bungalows with breakfast and snorkeling packages.',
            'image': 'https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=1200&q=80'
        },
        {
            'title': 'Adventure & Active Tours',
            'desc': 'Multi-day active itineraries with local guides and gear.',
            'image': 'https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1200&q=80'
        }
    ]
    return render_template('deals.html', deals=featured)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # ensure data folder
        data_dir = os.path.join(app.root_path, 'data')
        os.makedirs(data_dir, exist_ok=True)
        with open(os.path.join(data_dir, 'contacts.txt'), 'a', encoding='utf-8') as f:
            f.write(f"{datetime.utcnow().isoformat()} | {name} | {email} | {message}\n")
        return render_template('contact_thanks.html', name=name)
    return render_template('contact.html')


@app.route('/db')
def db_schema():
    # show counts and link to schema
    client_count = Client.query.count()
    booking_count = Booking.query.count()
    return render_template('db_schema.html', clients=client_count, bookings=booking_count)

@app.route('/bookings/new', methods=['GET','POST'])
def new_booking():
    if request.method == 'POST':
        client = Client(
            name=request.form['client_name'],
            email=request.form['client_email'],
            phone=request.form['client_phone'],
            company=request.form['client_company']
        )
        db.session.add(client)
        db.session.flush()

        booking = Booking(
            booking_code=request.form['booking_code'],
            destination=request.form['destination'],
            travel_date=datetime.strptime(request.form['travel_date'], '%Y-%m-%d').date(),
            status=request.form['status'],
            notes=request.form['notes'],
            client_id=client.id
        )
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_booking.html')

@app.route('/bookings/<int:booking_id>/edit', methods=['GET','POST'])
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if request.method == 'POST':
        booking.booking_code = request.form['booking_code']
        booking.destination = request.form['destination']
        booking.travel_date = datetime.strptime(request.form['travel_date'], '%Y-%m-%d').date()
        booking.status = request.form['status']
        booking.notes = request.form['notes']
        booking.client.name = request.form['client_name']
        booking.client.email = request.form['client_email']
        booking.client.phone = request.form['client_phone']
        booking.client.company = request.form['client_company']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_booking.html', booking=booking)

@app.route('/bookings/<int:booking_id>/delete', methods=['POST'])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
