from decimal import Decimal
from unittest import mock

import pytest

from hypothesis.models import Transaction, Customer


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
    assert transaction.customer_source_value == source.balance == Decimal('-50')
    assert transaction.customer_target_value == target.balance == Decimal('50')


@pytest.mark.usefixtures('session')
def test_create_transaction_customer_doesnt_exist(client, headers, transaction_payload):
    transaction_payload['customer_source'] = 999
    transaction_payload['customer_target'] = 1000

    response = client.post(
        '/transactions/', json=transaction_payload, headers=headers
    )

    transaction = Transaction.query.first()

    expected_response = {'_schema': ['Invalid identifier(s), customer(s) not found']}

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert not transaction
    assert response.json['error'] == expected_response

@pytest.mark.usefixtures('session')
def test_create_transaction_customer_shouldnt_be_the_same(client, headers, transaction_payload):
    transaction_payload['customer_source'] = 999
    transaction_payload['customer_target'] = 999

    response = client.post(
        '/transactions/', json=transaction_payload, headers=headers
    )

    transaction = Transaction.query.first()

    expected_response = {'_schema': ['Customers should not be the same to create a transaction']}

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert not transaction
    assert response.json['error'] == expected_response

#
#@pytest.mark.usefixtures('session')
#@pytest.mark.parametrize(
#    'field,value,expected_response',
#    [
#        ('name', None, {'name': ['Field may not be null.']}),
#        ('name', {}, {'name': ['Not a valid string.']}),
#        ('name', 'pizza' * 11, {'name': ['Length must be between 1 and 50.']}),
#        ('name', '', {'name': ['Length must be between 1 and 50.']}),
#        ('name', 20.1, {'name': ['Not a valid string.']}),
#    ],
#)
#def test_create_customer_badrequest(
#    client, headers, customer_payload, field, value, expected_response
#):
#    customer_payload[field] = value
#    response = client.post(
#        '/customers/', json=customer_payload, headers=headers
#    )
#
#    assert response.status_code == 400
#    assert response.json['error'] == expected_response
#
#
#@pytest.mark.usefixtures('session', 'customers_saved')
#def test_list_customers(client, headers):
#    response = client.get('/customers/', headers=headers)
#
#    content = response.json
#
#    assert response.status_code == 200
#    assert len(content) == 20
#    assert content[0]['name'] == 'pizza-planet-0'
#    assert content[19]['name'] == 'pizza-planet-19'
#
#
#@pytest.mark.usefixtures('session', 'customers_saved')
#def test_list_customers_search_by_name(client, headers):
#    response = client.get('/customers/?name=planet-1', headers=headers)
#
#    content = response.json
#
#    assert response.status_code == 200
#    assert len(content) == 11
#    for x, i in zip(range(12), [1] + [a for a in range(10, 20)]):
#        assert content[x]['name'] == f'pizza-planet-{i}'
#
#
#@pytest.mark.usefixtures('session', 'customers_saved')
#def test_list_customers_search_by_identifier(client, headers):
#    response = client.get('/customers/?id=50', headers=headers)
#
#    content = response.json
#
#    assert response.status_code == 200
#    assert len(content) == 1
#    assert content[0]['name'] == 'pizza-planet-49'
