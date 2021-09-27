from decimal import Decimal
from unittest import mock

import pytest

from hypothesis.models import Customer, Transaction


@pytest.mark.usefixtures('session')
def test_create_transaction_with_success(client, headers, transaction_payload):
    response = client.post(
        '/transactions/', json=transaction_payload, headers=headers
    )

    transaction = Transaction.query.first()
    source = Customer.query.get(transaction.customer_source)
    target = Customer.query.get(transaction.customer_target)

    content = response.json

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert transaction._id == content['_id']
    assert transaction.customer_source == content['customer_source']
    assert transaction.customer_target == content['customer_target']
    assert transaction.value == Decimal('50')
    assert (
        transaction.customer_source_value == source.balance == Decimal('-50')
    )
    assert transaction.customer_target_value == target.balance == Decimal('50')


@pytest.mark.usefixtures('session')
def test_create_transaction_customer_doesnt_exist(
    client, headers, transaction_payload
):
    transaction_payload['customer_source'] = 999
    transaction_payload['customer_target'] = 1000

    response = client.post(
        '/transactions/', json=transaction_payload, headers=headers
    )

    transaction = Transaction.query.first()

    expected_response = {
        '_schema': ['Invalid identifier(s), customer(s) not found']
    }

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert not transaction
    assert response.json['error'] == expected_response


@pytest.mark.usefixtures('session')
def test_create_transaction_customer_shouldnt_be_the_same(
    client, headers, transaction_payload
):
    transaction_payload['customer_source'] = 999
    transaction_payload['customer_target'] = 999

    response = client.post(
        '/transactions/', json=transaction_payload, headers=headers
    )

    transaction = Transaction.query.first()

    expected_response = {
        '_schema': ['Customers should not be the same to create a transaction']
    }

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert not transaction
    assert response.json['error'] == expected_response


@pytest.mark.usefixtures('session')
@pytest.mark.parametrize(
    'field,value,expected_response',
    [
        (
            'customer_source',
            'xyz',
            {'customer_source': ['Not a valid integer.']},
        ),
        (
            'customer_source',
            None,
            {'customer_source': ['Field may not be null.']},
        ),
        ('customer_source', {}, {'customer_source': ['Not a valid integer.']}),
        (
            'customer_target',
            'xyz',
            {'customer_target': ['Not a valid integer.']},
        ),
        (
            'customer_target',
            None,
            {'customer_target': ['Field may not be null.']},
        ),
        ('customer_target', {}, {'customer_target': ['Not a valid integer.']}),
        ('value', 'xyz', {'value': ['Not a valid number.']}),
        ('value', None, {'value': ['Field may not be null.']}),
        ('value', {}, {'value': ['Not a valid number.']}),
        ('value', -10, {'value': ['Must be greater than 0.']}),
        ('value', 0, {'value': ['Must be greater than 0.']}),
    ],
)
def test_create_transaction_badrequest_invalid_data_type(
    client, headers, transaction_payload, field, value, expected_response
):
    transaction_payload[field] = value

    response = client.post(
        '/transactions/', json=transaction_payload, headers=headers
    )

    transaction = Transaction.query.first()

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert not transaction
    assert response.json['error'] == expected_response


@pytest.mark.usefixtures('session')
@pytest.mark.parametrize(
    'field,expected_response',
    [
        (
            'customer_source',
            {'customer_source': ['Missing data for required field.']},
        ),
        (
            'customer_target',
            {'customer_target': ['Missing data for required field.']},
        ),
        ('value', {'value': ['Missing data for required field.']}),
    ],
)
def test_create_transaction_badrequest_when_required_fields_are_ignored(
    client, headers, transaction_payload, field, expected_response
):
    del transaction_payload[field]

    response = client.post(
        '/transactions/', json=transaction_payload, headers=headers
    )

    transaction = Transaction.query.first()

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert not transaction
    assert response.json['error'] == expected_response


@pytest.mark.usefixtures('session', 'transactions_saved')
def test_list_transactions(client, headers):
    response = client.get('/transactions/', headers=headers)

    content = response.json

    assert response.status_code == 200
    assert len(content) == 20


@pytest.mark.usefixtures('session', 'transactions_saved')
def test_list_transactions_search_by_customer_id(client, headers):
    response = client.get('/transactions/?customer_id=100', headers=headers)

    content = response.json

    import ipdb

    ipdb.set_trace()
    assert response.status_code == 200
    assert len(content) == 20


#    for x, i in zip(range(12), [1] + [a for a in range(10, 20)]):
#        assert content[x]['name'] == f'pizza-planet-{i}'


# @pytest.mark.usefixtures('session', 'customers_saved')
# def test_list_customers_search_by_identifier(client, headers):
#    response = client.get('/customers/?id=50', headers=headers)
#
#    content = response.json
#
#    assert response.status_code == 200
#    assert len(content) == 1
#    assert content[0]['name'] == 'pizza-planet-49'
