
# History

## 0.3.0 (2016-12-29)

* Retry publishing to hermes in case of failure (default: 3x)
* Support for Python3.6, Django 1.10 and Django development version in tests


## 0.2.1 (2016-12-12)

* Configure custom label for django app #11


## 0.2.0 (2016-11-03)

* Fix ambiguity with pyhermes.decorators.subscriber (rename subscriber module to subscription)


## 0.1.3 (2016-06-21)

* Allow for custom wrapper around subcriber function
* Additional logging for event id and retry count
* Added support for Django <= 1.7
* Raw data is dumped only to debug logs.


## 0.1.2 (2016-04-20)

* New management command for testing Hermes connection


## 0.1.0 (2016-04-13)

* First release on PyPI.
