# Configuration

Possible configuration options for `pyhermes` are listed below.

## `BASE_URL`

Specifies base URL of Hermes. Example:
```python
BASE_URL = 'http://my-hermes.local'
```

## `URL_ADAPTER`

Set this to any callable, if you want to add additional adapter for hermes requests (it's usefull when you're using service discovery, like [Consul](https://www.consul.io/)). Example usage (with [requests-consul](https://github.com/RulersOfAsgard/requests-consul) library):
```python
def consul_adapter():
    from requests_consul.adapters.service import ConsulServiceAdapter
    return 'service://', ConsulServiceAdapter(**CONSUL)

BASE_URL = 'service://hermes'
URL_ADAPTER = consul_adapter
```

## `RETRY_MAX_ATTEMTPS`

Specify how many times pyhermes should retry communication with Hermes. Default: 3

## `PUBLISHING_GROUP`
Configuration of Hermes group to which you application will publish messages. Keys of this dictionary are the same as in [Hermes creating group](http://hermes-pubsub.readthedocs.org/en/latest/user/publishing/#creating-group) request body. Example:
```python
PUBLISHING_GROUP = {
    'groupName': 'pl.allegro.pyhermes',
    'supportTeam': 'pyLabs',
    'owner': 'pyLabs',
    'contact': 'pylabs@allegro.pl'
}
```

## `PUBLISHING_TOPICS`
Configuration of topics to which messages will be published from your application. Key of the main dictionary is name of the topic. Keys of single topic configuration are the same as in [Hermes creating topic](http://hermes-pubsub.readthedocs.org/en/latest/user/publishing/#creating-topic) request body. Example:
```python
PUBLISHING_TOPICS = {
    'test1': {
        'description': "test topic",
        'ack': 'LEADER',
        'retentionTime': 1,
        'trackingEnabled': False,
        'contentType': 'JSON',
        'validationEnabled': False,
    }
}
```

> You don't have to specify all properties for single topic, just like in [Hermes creating topic](http://hermes-pubsub.readthedocs.org/en/latest/user/publishing/#creating-topic) request body.

> Note that full topic name for publishing will be combination of publish group name (`PUBLISHING_GROUP['groupName']`) and topic name, for example `pl.allegro.pyhermes.test1`.

## `SUBSCRIBERS_MAPPING`
Here you could define mapping for subscribed topics. Example:

```python
SUBSCRIBERS_MAPPING = {
    'pl.allegro.pyhermes.test1': 'my-topic'
}
```

Then you could use mapped topic for your subscriptions:

```python
import pyhermes

@pyhermes.subscriber(topic='my-topic')
def my_handler(data):
    pass
```

In this case, `my_handler` will be used for every message coming for `pl.allegro.pyhermes.test1` topic.
