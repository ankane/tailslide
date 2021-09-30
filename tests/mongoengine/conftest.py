from mongoengine import connect, DecimalField, Document, FloatField, IntField, StringField
from tailslide.mongoengine import TailslideQuerySet

connect('tailslide_test')


class User(Document):
    visits_count = IntField()
    latitude = DecimalField(precision=5)
    rating = FloatField()
    name = StringField()

    meta = {'queryset_class': TailslideQuerySet}
