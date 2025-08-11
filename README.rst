Payload API
===============

A simple Django REST Framework application that receives IoT device payloads, validates them, decodes their data, and stores the results.

Features
--------

* **Token Authentication** using Django REST Framework's TokenAuth
* **Device** and **Payload** models with one-to-many relationship
* Duplicate payload prevention via ``fCnt`` unique constraint
* Base64 ``data`` decoding into hexadecimal
* Automatic pass/fail status determination based on decoded data
* Device latest status tracking

Example Payload
---------------

.. code-block:: json

    {
        "fCnt": 100,
        "devEUI": "abcdabcdabcdabcd",
        "data": "AQ==",
        "rxInfo": [
            {
                "gatewayID": "1234123412341234",
                "name": "G1",
                "time": "2022-07-19T11:00:00",
                "rssi": -57,
                "loRaSNR": 10
            }
        ],
        "txInfo": {
            "frequency": 86810000,
            "dr": 5
        }
    }

Decoded Data Rules
------------------

* Base64 ``data`` → Hexadecimal string
* If hex value is ``01`` → **passing**
* Otherwise → **failing**

Installation
------------

1. **Clone the repository**:

   .. code-block:: bash

       git clone https://github.com/mattjgerace/coding-challenge-1.git
       cd coding-challenge-1

2. **Create a virtual environment and activate it**:

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate  # macOS/Linux
       venv\Scripts\activate     # Windows

3. **Install dependencies**:

   .. code-block:: bash

       pip install -r requirements.txt

4. **Run migrations**:

   .. code-block:: bash

       python manage.py migrate

5. **Create a superuser** (for admin access):

   .. code-block:: bash

       python manage.py createsuperuser

6. **Start the development server**:

   .. code-block:: bash

       python manage.py runserver

Authentication
--------------

This API uses **Token Authentication**.

1. Obtain a token:

   .. code-block:: bash

       curl -X POST http://127.0.0.1:8000/api/token/ \
       -d "username=<your_username>&password=<your_password>"

   Response:

   .. code-block:: json

       {"token": "your_token_here"}

2. Use the token in requests:

   .. code-block:: bash

       curl -X POST http://127.0.0.1:8000/api/payloads/ \
       -H "Authorization: Token your_token_here" \
       -H "Content-Type: application/json" \
       -d '{...payload JSON...}'

Endpoints
---------

* ``POST /api/token/`` – Obtain token
* ``POST /api/payloads/`` – Submit a payload
* ``GET /api/payloads/`` – List all payloads (authenticated)
* ``GET /api/payloads/{id}/`` – Retrieve a single payload