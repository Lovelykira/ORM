import MySQLdb
import MySQLdb.cursors


class DB:
    def __init__(self):
        self.connection = MySQLdb.connect(user='root',
                                     passwd='123',
                                     db='db',
                                     cursorclass=MySQLdb.cursors.DictCursor)

    def execute(self, str):
        cursor = self.connection.cursor()
        cursor.execute(str)
        self.connection.commit()
        return cursor.fetchall()

    def migrate(self, cls):
        cls_name = cls.__name__
        attributes = cls.get_attributes()
        attributes_str = ""
        for key, value in attributes.items():
            if attributes_str:
                attributes_str = "{}, ".format(attributes_str)
            attributes_str = "{}{} {}".format(attributes_str, key, value)
        sql_query = 'CREATE TABLE IF NOT EXISTS {} ({});'.format(cls_name, attributes_str)
        print(sql_query)
        return self.execute(sql_query)

    def insert(self, obj):
        cls_name = obj.__class__.__name__
        columns = obj.get_attributes().keys()
        values = []
        for column in columns:
            if isinstance(getattr(obj, column), str):
                values.append("'{}'".format(getattr(obj, column)))
            else:
                values.append(str(getattr(obj, column)))
        columns = ', '.join(columns)
        values = ', '.join(values)
        sql_query = "INSERT INTO {} ({}) VALUES ({});".format(cls_name, columns, values)
        print(sql_query)
        return self.execute(sql_query)

    def select(self, table, **kwargs):
        table_name = table.__name__
        parameters = ""
        for key, value in kwargs.items():
            if isinstance(value, str):
                value="'{}'".format(value)
            if "__" in key:
                operator = ""
                if 'contains' in key.split("__")[1]:
                    operator = 'LIKE'
                else:
                    if 'lt' in key.split("__")[1]:
                        operator += '<'
                    if 'gt' in key.split("__")[1]:
                        operator += '>'
                    if 'e' in key.split("__")[1]:
                        operator += '='
                if parameters:
                    parameters += " AND "
                parameters = "{}{} {} {}".format(parameters, key.split("__")[0], operator, str(value))
            else:
                if parameters:
                    parameters += " AND "
                parameters = "{}{} = {}".format(parameters, key, str(value))

        if len(kwargs) != 0:
            sql_query = 'SELECT * FROM {} WHERE {};'.format(table_name, parameters)
        else:
            sql_query = 'SELECT * FROM {};'.format(table_name)
        print(sql_query)
        return self.execute(sql_query)

