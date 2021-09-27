import logging
from datetime import datetime

import flask
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

from hypothesis.factory import db
from hypothesis.exceptions import APIError
from hypothesis.settings import Configuration
from hypothesis.models import Transaction, Customer
from hypothesis.schemas import TransactionSchema, CustomerSchema

blueprint = Blueprint('api', __name__)

logger = logging.getLogger(__name__)


@blueprint.route('/transactions/', methods=['GET', 'POST'])
def transactions():
    schema = TransactionSchema()
    if request.method == 'POST':

        try:
            payload = request.get_json()
            data = schema.load(payload)

            transaction = Transaction(**data)

            # update source and target balance as well
            # see if is possible pass more transactions to add
            db.session.add(transaction)
            db.session.commit()
    
        except Exception as e:
            import ipdb; ipdb.set_trace();
            pizza = e
        
        transactions = schema.dump(transaction)
    
    else:
        # search by customer
        # search by date
        # pagination
        import ipdb; ipdb.set_trace();
        transactions = [ schema.dump(t) for t in Transaction.query.all() ]


    return jsonify(transactions)

@blueprint.route('/customers/', methods=['GET', 'POST'])
def customers():

    status_code = 200
    schema = CustomerSchema()
    
    if request.method == 'POST':

        try:
            payload = request.get_json()
            data = schema.load(payload)

            customer = Customer(**data)

            db.session.add(customer)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            status_code = 409
            response = {'error': 'Customer already exists'}
        except ValidationError as e:
            status_code = 400
            response = {'error': e.args[0]}
        else:
            response = schema.dump(customer)
            status_code = 201
    else:
        query_string = request.args.to_dict()
        query = Customer.query
       
        page = query_string.get('page')
        if not isinstance(page, int):
            page = 1

        if query_string.get('id'):
            query = query.filter_by(_id=query_string['id'])
        elif query_string.get('name'):
            query = query.filter(Customer.name.contains(
                query_string['name']
            ))
        
        response = [ 
                schema.dump(t) 
                for t in query.paginate(page, 20).items 
        ]


    return jsonify(response), status_code
