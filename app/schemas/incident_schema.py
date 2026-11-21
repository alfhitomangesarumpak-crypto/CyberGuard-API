from marshmallow import Schema, fields, validate

class IncidentSchema(Schema):
    id = fields.Int(dump_only=True)
    asset_id = fields.Int(required=True)
    reported_by = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=3, max=150))
    incident_type = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    severity = fields.Str(required=True, validate=validate.OneOf(['low', 'medium', 'high', 'critical']))
    status = fields.Str(validate=validate.OneOf(['open', 'investigating', 'resolved']), load_default='open')
    description = fields.Str(allow_none=True)
    reported_at = fields.DateTime(dump_only=True)