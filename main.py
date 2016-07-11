from abstract_model import AbstractModel
from db_field import StringField, IntField, BoolField, FloatField
from data_base import DB


class Person(AbstractModel):
    name = StringField(length=200)
    age = IntField()
    b = BoolField()
    f = FloatField()


if __name__ == "__main__":
    pers1 = Person(name='Nata', age=14, b=True, f=3.5)
    pers2 = Person(name='Stas', age=15, b=False, f=10.2)
    pers3 = Person(name='Hina', age=16, b=True, f=123.4)
    database = DB()
    database.migrate(Person)
    database.insert(pers1)
    database.insert(pers2)
    database.insert(pers3)
    print(database.select(Person))
    print(database.select(Person, age__lte=14, name='Nata' ))
    print(database.select(Person, b__contains=False, age__gt=1))
    print(database.select(Person, b__contains=True, f__gte=123))
    print(database.select(Person, b__contains=True))
