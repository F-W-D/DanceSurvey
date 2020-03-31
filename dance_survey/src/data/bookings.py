import mongoengine


class Booking(mongoengine.EmbeddedDocument):
    guest_studio_id = mongoengine.ObjectIdField()
    guest_teacher_id = mongoengine.ObjectIdField()
    guest_dancer_ids = mongoengine.ListField()

    booked_date = mongoengine.DateTimeField()
    check_in_date = mongoengine.DateTimeField(required=True)
    check_out_date = mongoengine.DateTimeField(required=True)

    review = mongoengine.StringField()
    rating = mongoengine.IntField(default=0)

    @property
    def duration_in_days(self):
        dt = self.check_out_date - self.check_in_date
        return dt.days
