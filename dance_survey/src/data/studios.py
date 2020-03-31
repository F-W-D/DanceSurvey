import datetime
import mongoengine

from data.bookings import Booking


class Studio(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)

    name = mongoengine.StringField(required=True)
    price = mongoengine.FloatField(required=True)
    square_meters = mongoengine.FloatField(required=True)
    is_rentable = mongoengine.BooleanField(required=True)
    number_of_rooms = mongoengine.IntField(required=True)
    allows_adults = mongoengine.BooleanField(default=False)

    bookings = mongoengine.EmbeddedDocumentListField(Booking)

    meta = {
        'db_alias': 'core',
        'collection': 'studios'
    }
