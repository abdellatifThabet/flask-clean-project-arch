from marshmallow import Schema, fields


class BookSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    book_price = fields.Integer()