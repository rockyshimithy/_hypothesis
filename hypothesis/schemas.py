from datetime import datetime

from marshmallow import (
    EXCLUDE,
    Schema,
    ValidationError,
    fields,
    post_load,
    pre_load,
)
from marshmallow.validate import Length, Range

from hypothesis.models import Customer


class TransactionSchema(Schema):
    _id = fields.Integer(attribute='_id')
    datetime = fields.DateTime()
    customer_source = fields.Integer(required=True)
    customer_target = fields.Integer(required=True)
    value = fields.Float(
        required=True, validate=Range(min=0, min_inclusive=False)
    )
    customer_source_value = fields.Float()
    customer_target_value = fields.Float()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def prepare_object(self, data, **kwargs):
        data['datetime'] = datetime.now().isoformat()

        if data['customer_source'] == data['customer_target']:
            raise ValidationError(
                'Customers should not be the same to create a transaction'
            )

        data['source_obj'] = Customer.query.get(data['customer_source'])
        data['target_obj'] = Customer.query.get(data['customer_target'])

        if not data['source_obj'] or not data['target_obj']:
            raise ValidationError(
                'Invalid identifier(s), customer(s) not found'
            )

        data['customer_source'] = data['source_obj']._id
        data['customer_target'] = data['target_obj']._id

        data['customer_source_value'] = (
            float(data['source_obj'].balance) - data['value']
        )
        data['customer_target_value'] = (
            float(data['target_obj'].balance) + data['value']
        )
        return data


class CustomerSchema(Schema):
    _id = fields.Integer(attribute='_id')
    name = fields.String(required=True, validate=Length(min=1, max=50))
    balance = fields.Float()

    class Meta:
        unknown = EXCLUDE
