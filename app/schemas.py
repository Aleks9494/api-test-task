from marshmallow import Schema, validate, fields


class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)  # только для сериализации (вывода)
    title = fields.String(required=True, validate=[validate.Length(max=40)])
    body = fields.String(required=True, validate=[validate.Length(max=100)])
    date_to_do = fields.Date(required=True)
    mark = fields.Boolean()


class UpdateTaskSchema(Schema):
    mark = fields.Boolean(required=True)

