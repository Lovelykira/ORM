class DbField:
    sql_type = None

    def get_sql_type(self):
        return self.sql_type


class StringField(DbField):
    sql_type = 'varchar'

    def __init__(self, length):
        self.max_length = length

    def get_sql_type(self):
        return '{}({})'.format(self.sql_type, self.max_length)


class IntField(DbField):
    sql_type = 'int'


class FloatField(DbField):
    sql_type = 'float'


class BoolField(DbField):
    sql_type = 'bool'