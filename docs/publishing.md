# Publishing

## `publish` function
Use `pyhermes.publish` function to publish messages to Hermes.

```python
import pyhermes

@pyhermes.publisher(topic='sample-topic')
def my_function():
    # processing
    pyhermes.publish(my_function._topic, {'result': result})
```

> Note that after using `pyhermes.publisher` decorator, `_topic` attribute with the name of the topic is assigned to your function.

## autopublishing result of the function
You could use `auto_publish_result` param to automatically publish result of the function to the given topic.

```python
@pyhermes.publisher(topic='sample-topic', auto_publish_result=True)
def my_function():
    return {'result': 'abc'}
```

In this case, `{'result': 'abc'}` will be published with `sample-topic` topic after execution of the function.

> Note that result of the function has to be JSON-serializable.
