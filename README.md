# FastAPI Bug

## Steps to recreate

Install dependencies; either:

```shell
pip install 'fastapi[standard]' pytest
```

or:

```shell
pip install -r requirements.txt
```

Run the tests:

```shell
pytest
```

or start the app:

```shell
python -m app
```
and hit the endpoints, e.g. using:
```shell
curl --header 'Request-Correlation-Id: whatever' --verbose 'http://0.0.0.0:8080/success'
```
