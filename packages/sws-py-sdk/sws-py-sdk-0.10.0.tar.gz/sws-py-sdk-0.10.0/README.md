## Welcome to the Serato Web Service Python SDK.

This SDK exists to make it easier for Python based applications and clients to consume SWS (Serato Web Service) endpoints.

### Installing SWS-Py-SDK

I recommend using `Pipenv` for this project.

Then install the SDK with the following command:


```
pipenv install sws_py_sdk
```

Then you should be good to go.


### Running tests

The tests are split into two groups, `spec` and `integration`.
`spec` tests test the functionality and features of the internal SDK, i.e, the `service` and `sws_client`.

The `integration` tests check that the endpoints implemented are sane. This means they exist (non-404) and are acceptable request (non-500).

The tests are run with Pytest and assume that you have your local vagrant machines running for each service.

Run the tests with:

```
pipenv install --dev
pipenv run python -m pytest
```

This will collect all the tests and run them.

