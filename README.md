## pyhermes

[![Version Badge](https://badge.fury.io/py/pyhermes.png)](https://badge.fury.io/py/pyhermes.png)
[![Build Status](https://travis-ci.org/allegro/pyhermes.png?branch=master)](https://travis-ci.org/allegro/pyhermes)

The Python interface to the [Hermes](http://hermes.allegro.tech) message broker.

## Documentation

The full documentation is at https://pyhermes.readthedocs.org.

## Installation

To install pyhermes, simply:

```python
pip install pyhermes
```

Then use it in a project:

```python
import pyhermes
```

## Features

* TODO

## Quickstart

### Subscriber

To create handler for particular subscription topic decorate your function using `subscribe` decorator:

```python
import pyhermes

@pyhermes.subscriber(topic='pl.allegro.pyhermes.sample-topic')
def handler(data):
    # process data
```

This function will be called every time there is new message published to the selected topic.

### Publisher
Use `publish` function to publish data to some topic in hermes:

```python
import pyhermes

@pyhermes.publisher(topic='pl.allegro.pyhermes.sample-topic')
def my_complex_function(a, b, c):
    result = a + b + c
    publish(my_complex_function._topic, {'complex_result': result})
```

You could publish directly result of the function as well:

```python
import pyhermes

@pyhermes.publisher(topic='pl.allegro.pyhermes.sample-topic', auto_publish_result=True)
def my_complex_function(a, b, c):
    return {'complex_result': a + b + c}
```

Result of decorated function is automatically published to selected topic in hermes.

## Running Tests

Does the code actually work?

```python
source <YOURVIRTUALENV>/bin/activate
(myenv) $ pip install -r requirements-test.txt
(myenv) $ python runtests.py
```

## Credits

Tools used in rendering this package:

*  [Cookiecutter](https://github.com/audreyr/cookiecutter)
*  [cookiecutter-djangopackage](https://github.com/pydanny/cookiecutter-djangopackage)
