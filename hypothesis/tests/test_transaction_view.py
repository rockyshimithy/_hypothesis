from decimal import Decimal
from unittest import mock

import pytest

from hypothesis.models import Transaction


@pytest.mark.usefixtures('session')
def test_create_transaction_with_success(client, headers, transaction_payload):
    response = client.post(
        '/transactions/', json=transaction_payload, headers=headers
    )

    transaction = Transaction.first()

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert transaction.name == transaction_payload['name']
    assert transaction.balance == 0.0
#
#
#@pytest.mark.usefixtures('session')
#def test_create_customer_with_balance_success(
#    client, headers, customer_payload
#):
#    customer_payload['balance'] = 50.0505560
#    response = client.post(
#        '/customers/', json=customer_payload, headers=headers
#    )
#
#    customer = Customer.query.filter_by(name=customer_payload['name']).first()
#
#    assert response.status_code == 201
#    assert response.headers['Content-Type'] == 'application/json'
#    assert customer.name == customer_payload['name']
#    assert float(customer.balance) == response.json['balance']
#    assert customer.balance == Decimal('50.05')
#
#
#@pytest.mark.usefixtures('session', 'customers_saved')
#def test_create_customer_failed_already_exists(
#    client, headers, customer_payload
#):
#    response = client.post(
#        '/customers/', json=customer_payload, headers=headers
#    )
#
#    customer = Customer.query.filter_by(name=customer_payload['name']).first()
#
#    assert response.status_code == 409
#    assert response.headers['Content-Type'] == 'application/json'
#    assert response.json['error'] == 'Customer already exists'
#
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
