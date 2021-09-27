import logging
from datetime import datetime

import flask
from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from hypothesis.exceptions import APIError
from hypothesis.factory import db
from hypothesis.models import Customer, Transaction
from hypothesis.schemas import CustomerSchema, TransactionSchema
from hypothesis.settings import Configuration

blueprint = Blueprint('api', __name__)

logger = logging.getLogger(__name__)


@blueprint.route('/transactions/', methods=['GET', 'POST'])
def transactions():
    query = Transaction.query
    schema = TransactionSchema()
    status_code = 200

    if request.method == 'POST':
        try:
            payload = request.get_json()
            data = schema.load(payload)

            source = data.pop('source_obj')
            target = data.pop('target_obj')
            source.balance = data['customer_source_value']
            target.balance = data['customer_target_value']

            transaction = Transaction(**data)

            db.session.add(transaction)
            db.session.commit()
        except ValidationError as e:
            status_code = 400
            response = {'error': e.args[0]}
        except Exception as e:
            import ipdb;ipdb.set_trace()
            pizza = e
        else:
            status_code = 201
            response = schema.dump(transaction)
    else:
        query_string = request.args.to_dict()

        page = query_string.get('page')
        if not isinstance(page, int):
            page = 1

        if query_string.get('date'):
            import ipdb;ipdb.set_trace()
            query = query.filter(
                Transaction.datetime == query_string['date']
            )  # TODO
        if query_string.get('customer_id'):
            import ipdb;ipdb.set_trace()
            query = query.filter(
                or_(
                    Transaction.customer_source == query_string['customer_id'],
                    Transaction.customer_target == query_string['customer_id'],
                )
            )  # TODO

        response = [schema.dump(t) for t in query.paginate(page, 20).items]

    return jsonify(response), status_code


@blueprint.route('/customers/', methods=['GET', 'POST'])
def customers():
    query = Customer.query
    schema = CustomerSchema()
    status_code = 200

    if request.method == 'POST':
        try:
            payload = request.get_json()
            data = schema.load(payload)

            customer = Customer(**data)

            db.session.add(customer)
            db.session.commit()
        except ValidationError as e:
            status_code = 400
            response = {'error': e.args[0]}
        except IntegrityError:
            db.session.rollback()
            status_code = 409
            response = {'error': 'Customer already exists'}
        else:
            status_code = 201
            response = schema.dump(customer)
    else:
        query_string = request.args.to_dict()

        page = query_string.get('page')
        if not isinstance(page, int):
            page = 1

        if query_string.get('id'):  # test to filter with others values
            query = query.filter_by(_id=query_string['id'])
        elif query_string.get('name'):
            query = query.filter(Customer.name.contains(query_string['name']))

        response = [schema.dump(c) for c in query.paginate(page, 20).items]

    return jsonify(response), status_code
