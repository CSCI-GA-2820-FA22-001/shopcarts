# NYU DevOps Project - Shopcarts

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-FA22-001/shopcarts/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA22-001/shopcarts/actions)
[![Build Status](https://github.com/CSCI-GA-2820-FA22-001/shopcarts/actions/workflows/bdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA22-001/shopcarts/actions)

This is a class project for *DevOps and Agile Methodologies (CSCI-GA.2820)* at
New York University, taught by Professor John Rofrano.

## Overview

This project is one of the 8 RESTful microservices that are part of an eCommerce
application. We adopt DevOps, Agile and Test Driven Development methodologies during this class.

The `shopcarts` resource allow customers to make a collection of products that they want to purchase. It contains a reference to a product id, product name, and the quantity the customer wants to buy. It also contains the price of the product at the time it was placed in the cart.

## Team Members

- Hu, Weiqi
- Huang, Pin-Tsung
- Xia, Robin
- Bharti, Sweta
- Lu, Yuheng

## Usage
This service has a single page UI available at `/`, and there are also RESTful
APIs for integration of the application. The service provides a health endpoint
at `/health` too.

### `GET`
- List all Shopcarts: `GET /shopcarts`
- Read a Shopcart: `GET /shopcarts/<shopcart_id>`
- List all items in a Shopcart `GET /shopcarts/<shopcart_id>/items`
- Read an item in a Shopcart `GET /shopcarts/<shopcart_id>/items/<item_id>`

### `POST`
- Create a Shopcart: `POST /shopcarts`.
- Add an item to a Shopcart `POST /shopcarts/<shopcart_id>/items`

### `DELETE`
- Delete a Shopcart: `DELETE /shopcarts/<shopcart_id>`
- Delete an item in a Shopcart `DELETE /shopcarts/<shopcart_id>/items/<item_id>`

### `PUT`
- Update a Shopcart: `PUT /shopcarts/<shopcart_id>`
- Update an item in a Shopcart `PUT /shopcarts/<shopcart_id>/items/<item_id>`

The service also provides other Actions:
- Reset a Shopcart: `PUT /shopcarts/<shopcart_id>/reset`
- Checkout a Shopcart: `POST /shopcarts/<shopcart_id>/checkout`


## How To Test
We use `nosetests` and `behave`. Just run
```
nosetests
```
and
```
behave
```
and they will print the test results and coverage.


## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## Deployment

### First Time Deployment
* Open Docker on your local machine
* Open the code in Dev Container
* In terminal, use `make login` to login to IBM Cloud, authenticate with the container registry, and pull down the cluster configuration
* In terminal, use `make build` to build Docker images
* Then, in terminal, type in these three commands to deploy postgres db and all others and make the service run
  * `kubectl apply -n dev -f deploy/postgresql.yaml`
  * `kubectl create -n dev -f deploy/deployment.yaml`
  * `kubectl create -n dev -f deploy/service.yaml`

### After Deployment
* Open Docker on your local machine
* Open the code in Dev Container
* In terminal, use `make login` to login to IBM Cloud, authenticate with the container registry, and pull down the cluster configuration
* In terminal, use `kubectl -n dev get all` to see everything running under `dev` namespace
* In terminal, use `kubectl -n dev get service` to see services running under `dev` namespace
* In terminal, use `ibmcloud ks workers --cluster nyu-devops --output json | jq -r '.[0].publicIP'` to see the public IP
* Access the service through `WORKERNODE_PUBLIC_IP:31001`, replace the `WORKERNODE_PUBLIC_IP` with the public IP you got from the previous step

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
