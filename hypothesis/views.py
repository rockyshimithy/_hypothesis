import logging
from datetime import datetime

from marshmallow.exceptions import ValidationError
from sqlalchemy import Date, cast, or_
from sqlalchemy.exc import IntegrityError

from hypothesis.commons import BaseView
from hypothesis.factory import db
from hypothesis.models import Customer, Transaction
from hypothesis.schemas import CustomerSchema, TransactionSchema

logger = logging.getLogger(__name__)


class TransactionView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Transaction
        self.query = self.model.query
        self.schema = TransactionSchema()

    def get(self):
        """
        file: ../get_transactions.yml
        """
        super().get()

        if self.query_string.get('date'):
            self.query = self.query.filter(
                cast(self.model.datetime, Date)
                == datetime.strptime(self.query_string['date'], '%Y-%m-%d')
            )
        if self.query_string.get('customer_id'):
            self.query = self.query.filter(
                or_(
                    self.model.customer_source
                    == self.query_string['customer_id'],
                    self.model.customer_target
                    == self.query_string['customer_id'],
                )
            )

        return self.get_response()

    def post(self):
        """
        file: ../post_transaction.yml
        """
        try:
            super().post()

            source = self.data.pop('source_obj')
            target = self.data.pop('target_obj')
            source.balance = self.data['customer_source_value']
            target.balance = self.data['customer_target_value']

            transaction = Transaction(**self.data)

            db.session.add(transaction)
            db.session.commit()
        except ValidationError as e:
            self.status_code = 400
            response = {'error': e.args[0]}
        else:
            self.status_code = 201
            response = self.schema.dump(transaction)

        return self.response(response)


class CustomerView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Customer
        self.query = self.model.query
        self.schema = CustomerSchema()

    def get(self):
        """
        file: ../get_customers.yml
        """
        super().get()

        if self.query_string.get('id'):  # test to filter with others values
            self.query = self.query.filter_by(_id=self.query_string['id'])
        elif self.query_string.get('name'):
            self.query = self.query.filter(
                Customer.name.contains(self.query_string['name'])
            )

        return self.get_response()

    def post(self):
        """
        file: ../post_customer.yml
        """
        try:
            super().post()

            customer = Customer(**self.data)

            db.session.add(customer)
            db.session.commit()
        except ValidationError as e:
            self.status_code = 400
            response = {'error': e.args[0]}
        except IntegrityError:
            db.session.rollback()
            self.status_code = 409
            response = {'error': 'Customer already exists'}
        else:
            self.status_code = 201
            response = self.schema.dump(customer)

        return self.response(response)
