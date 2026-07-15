from app import db, Client, Booking
from datetime import date

def seed():
    if Client.query.count() > 0:
        print('Database already seeded')
        return
    c1 = Client(name='Alice Johnson', email='alice@example.com', phone='+1-868-555-0100', company='Sunrise Co')
    c2 = Client(name='John Peters', email='john@example.com', phone='+1-868-555-0111', company='Island Tours')
    db.session.add_all([c1,c2])
    db.session.flush()
    b1 = Booking(booking_code='ISL-0001', destination='Maldives', travel_date=date(2026,12,5), status='Confirmed', notes='Honeymoon package', client_id=c1.id)
    b2 = Booking(booking_code='ISL-0002', destination='Fiji', travel_date=date(2026,11,10), status='Pending', notes='Group retreat', client_id=c2.id)
    db.session.add_all([b1,b2])
    db.session.commit()
    print('Seeded sample clients and bookings')

if __name__ == '__main__':
    seed()
