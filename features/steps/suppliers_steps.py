"""
Supplier Steps

Steps file for suppliers.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import json
import requests
from behave import given
from compare import expect


@given('the following suppliers')
def step_impl(context):
    """ Delete all suppliers and load new ones """
    headers = {'Content-Type': 'application/json'}
    # list all of the suppliers and delete them one by one
    context.resp = requests.get(context.base_url + '/api/suppliers',
                                headers=headers)
    expect(context.resp.status_code).to_equal(200)
    for supplier in context.resp.json():
        context.resp = requests.delete(
            context.base_url+'/api/suppliers/'+str(supplier["id"]),
            headers=headers)
        expect(context.resp.status_code).to_equal(204)
    # load the database with new supplierss
    create_url = context.base_url + '/api/suppliers'
    for row in context.table:
        data = {
            "name": row['name'],
            "email": row['email'],
            "address": row['address'],
            "products": list(map(int, row['products'].split(","))) if row['products'] != "" else []
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)
