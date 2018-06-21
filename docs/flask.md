# Flask integration

`pyhermes` has built-in [Flask](http://flask.pocoo.org/) integration.

To use `pyhermes` together with Flask, follow these steps:

1. Add following code to your app:

```
from pyhermes.apps.flask import configure_pyhermes

configure_pyhermes(app, url_prefix='/hermes')
```

2. Configure `pyhermes` in flask config, for example:

```python
app.config['HERMES'] = {
    'BASE_URL': 'http://hermes.local',
    'PUBLISHING_GROUP': {
        'groupName': 'pl.allegro.pyhermes',
        'supportTeam': 'pyLabs',
        'owner': 'pyLabs',
        'contact': 'pylabs@allegro.pl'
    },
    'PUBLISHING_TOPICS': {
        'test1': {
            'description': "test topic",
            'ack': 'LEADER',
            'retentionTime': 1,
            'trackingEnabled': False,
            'contentType': 'JSON',
            'validationEnabled': False,
        }
    }
}
```

> Use `<YOUR-APP-URL>/hermes/events/<TOPIC-NAME>` (for example `http://my-flask-app.local/hermes/events/pl.allegro.pyhermes.test1`) to subscribe to particular topic in Hermes.


## Test command
After instalation you can test your configuration by following command:

```bash
flask hermes test
```

Command send message to all topics defined in settings to Hermes.
