from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time
from sqlalchemy import create_engine, inspect

from hypothesis.factory import create_app, db
from hypothesis.models import Customer, Transaction
from hypothesis.schemas import CustomerSchema, TransactionSchema

address = 'postgresql://postgres:postgres@127.0.0.1'
database = 'test_hypothesis'


def create_database():
    conn = create_engine(address, isolation_level='AUTOCOMMIT')

    database_already_exists = conn.execute(
        "SELECT exists(SELECT datname FROM "
        f"pg_catalog.pg_database where datname='{database}')"
    )

    if not database_already_exists.first()[0]:
        conn.execute(f'CREATE DATABASE {database}')

    return create_engine(f'{address}/{database}', isolation_level='AUTOCOMMIT')


@pytest.fixture(scope='session')
def app(request):
    testing_settings = {
        'TESTING': True,
        'PROPAGATE_EXCEPTIONS': True,
        'SQLALCHEMY_DATABASE_URI': f'{address}/{database}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    }

    app = create_app(settings_override=testing_settings)

    context = app.app_context()
    context.push()

    create_database()
    db.create_all()

    def teardown():
        db.session.remove()
        db.drop_all()
        context.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='function')
def session(request, app):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

    session = db.create_scoped_session(
        options={'bind': connection, 'binds': {}}
    )

    db.session = session

    def teardown():
        if transaction.is_active:
            db.session.query(Transaction).delete()
            db.session.query(Customer).delete()
            transaction.commit()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)


@pytest.fixture()
def headers():
    return {'Content-type': 'application/json'}


@pytest.fixture()
def customer_payload():
    return {'name': 'pizza-planet'}


@pytest.fixture()
def customers_saved(customer_payload):
    db.session.execute('TRUNCATE TABLE customer RESTART IDENTITY CASCADE')
    for i in range(98):
        customer_payload['name'] = f'pizza-planet-{i}'
        save_resource(CustomerSchema, Customer, customer_payload)

    customer_payload['name'] = 'company-x'
    save_resource(CustomerSchema, Customer, customer_payload)
    customer_payload['name'] = 'company-y'
    save_resource(CustomerSchema, Customer, customer_payload)


@pytest.fixture()
def transaction_payload(customers_saved):
    customer_source = Customer.query.filter_by(name='company-x').first()
    customer_target = Customer.query.filter_by(name='company-y').first()
    return {
        'customer_source': customer_source._id,
        'customer_target': customer_target._id,
        'value': 50,
    }


@pytest.fixture()
def transactions_saved(transaction_payload):
    date = datetime(2025, 4, 20)
    for i in range(1, 101):
        date += timedelta(hours=10)
        payload = {**transaction_payload}
        if i % 4 == 0:
            payload['customer_source'] = transaction_payload['customer_target']
            payload['customer_target'] = transaction_payload['customer_source']
            payload['value'] = i

        with freeze_time(date.strftime('%Y-%m-%d')):
            data = save_resource(TransactionSchema, Transaction, payload)
            data['source_obj'].balance = data['customer_source_value']
            data['target_obj'].balance = data['customer_target_value']
            db.session.commit()


def save_resource(schema, model, payload):
    data = schema().load(payload)
    mapper = inspect(model)
    model_object = model(
        **{k: v for k, v in data.items() if k in mapper.column_attrs.keys()}
    )
    db.session.add(model_object)
    db.session.commit()
    return data
