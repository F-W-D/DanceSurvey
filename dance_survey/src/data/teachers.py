import datetime
import mongoengine


class Teacher(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    age = mongoengine.IntField(required=True)
    is_friend = mongoengine.BooleanField(required=True)
    dance_style = mongoengine.StringField(required=True)
    dancer_ids = mongoengine.ListField()
    studio_ids = mongoengine.ListField()

    meta = {
        'db_alias': 'core',
        'collection': 'teachers'
    }
