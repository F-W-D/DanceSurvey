import datetime
import mongoengine


class Dancer(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    name = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    teacher_ids = mongoengine.ListField()
    studio_ids = mongoengine.ListField()

    meta = {
        'db_alias': 'core',
        'collection': 'dancers'
    }
