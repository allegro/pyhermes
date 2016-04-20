# Subscribing

Use `pyhermes.subscriber` decorator to mark your function as incoming message handlers.

```python
from pyhermes import subscriber

@subscriber(topic='sample-topic')
def handler(data):
    # process data
    ...
```
