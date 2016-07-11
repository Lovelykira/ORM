from db_field import DbField


class AbstractModel:
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    @classmethod
    def get_attributes(cls):
        attributes = {}
        for key, value in cls.__dict__.items():
            if issubclass(value.__class__, DbField):
                attributes[key] = value.get_sql_type()
        return attributes