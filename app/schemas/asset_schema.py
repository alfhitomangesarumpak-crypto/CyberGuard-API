from marshmallow import Schema, fields, validate

class AssetSchema(Schema):
    id = fields.Int(dump_only=True)
    asset_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    ip_address = fields.IP(required=True)
    asset_type = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    criticality = fields.Str(validate=validate.OneOf(['low', 'medium', 'high', 'critical']), load_default='medium')
    owner_department = fields.Str(required=True, validate=validate.Length(min=2, max=80))
    created_at = fields.DateTime(dump_only=True)