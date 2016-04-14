# Django integration

`pyhermes` has built-in [Django](https://www.djangoproject.com/) integration.

To use `pyhermes` together with Django, follow these steps:

1. Add `pyhermes` to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = (
    # other apps
    'pyhermes',
)
```

2. Configure `pyhermes` in `settings.py`:

```python
HERMES = {
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

3. Include `pyhermes.urls` in your `urls.py`:

```python
urlpatterns += patterns('',
    url(r'^hermes/', include('pyhermes.urls')),
)
```

> Use `<YOUR-APP-URL>/hermes/events/<TOPIC-NAME>` (for example `http://my-django-app.local/hermes/events/pl.allegro.pyhermes.test1`) to subscribe to particular topic in Hermes.
