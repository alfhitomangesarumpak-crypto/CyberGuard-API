from marshmallow import Schema, fields, validate

class IncidentResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    incident_id = fields.Int(required=True)
    responder_id = fields.Int(required=True)
    action_taken = fields.Str(required=True, validate=validate.Length(min=3, max=150))
    notes = fields.Str(allow_none=True)
    timestamp = fields.DateTime(dump_only=True)