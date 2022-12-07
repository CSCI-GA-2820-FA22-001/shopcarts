######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Shopcart Steps
Steps file for shopcarts.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
import json
from behave import given  # pylint: disable=no-name-in-module
from compare import expect


@given('the following shopcarts')
def step_impl(context):
    """ Delete all Shopcarts and load new ones """
    # List all of the shopcarts and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/shopcarts"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    existing_shopcarts = context.resp.json()['shopcarts']
    for shopcart in existing_shopcarts:
        context.resp = requests.delete(f"{rest_endpoint}/{shopcart['id']}")
        expect(context.resp.status_code).to_equal(204)

    shopcarts_id = []
    # load the database with new shopcarts
    for row in context.table:
        payload_shopcart = {
            "customer_id": row['customer_id'],
            "items": [],
        }
        context.resp = requests.post(rest_endpoint, json=payload_shopcart)
        shopcarts_id.append(int(context.resp.json()["id"]))
        expect(context.resp.status_code).to_equal(201)

    # load the database with new items
    for i, row in enumerate(context.table):
        row_lst = [json.loads(row['items'].replace("'", '"'))]
        for item in row_lst:
            payload_item = item[0]
            print(payload_item)
            print(type(payload_item))
            context.resp = requests.post(
                rest_endpoint+"/"+str(shopcarts_id[i])+"/items", json=payload_item)
            expect(context.resp.status_code).to_equal(201)
