from datetime import datetime

from marshmallow import EXCLUDE, Schema, fields, post_load, pre_load, validate
from marshmallow.validate import Length, Range

from hypothesis.models import Customer


class TransactionSchema(Schema):
    _id = fields.Integer(attribute='id')
    datetime = fields.DateTime()
    customer_source = fields.String(required=True)
    customer_target = fields.String(required=True)
    value = fields.Float(
        required=True, validate=Range(min=0, min_inclusive=False)
    )
    customer_source_value = fields.Float()
    customer_target_value = fields.Float()

    class Meta:
        unknown = EXCLUDE

    # validate if customers source and target exists and aren't the same
    @pre_load
    def checking_users(self, data, **kwargs):
        return data

    @post_load
    def prepare_object(self, data, **kwargs):
        data['datetime'] = datetime.now().isoformat()
        data[
            'customer_source_value'
        ] = 100  # to be calculate when customer model be created
        # calculate and provide customer_source_balance_value and customer_target_balance_value
        data['customer_target_value'] = 100
        return data


class CustomerSchema(Schema):

    _id = fields.Integer(attribute='id')
    name = fields.String(required=True, validate=Length(min=1, max=50))
    balance = fields.Float()

    class Meta:
        unknown = EXCLUDE
