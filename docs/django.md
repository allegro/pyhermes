# Django integration

`pyhermes` has built-in [Django](https://www.djangoproject.com/) integration.

To use `pyhermes` together with Django, follow these steps:

1. Add `pyhermes.apps.django` to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = (
    # other apps
    'pyhermes.apps.django',
)
```

2. Configure `pyhermes` in `settings.py`, for example:

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

3. Include `pyhermes.apps.django.urls` in your `urls.py`:

```python
urlpatterns += patterns('',
    url(r'^hermes/', include('pyhermes.apps.django.urls')),
)
```

> Use `<YOUR-APP-URL>/hermes/events/<TOPIC-NAME>` (for example `http://my-django-app.local/hermes/events/pl.allegro.pyhermes.test1`) to subscribe to particular topic in Hermes.


## Test command
After instalation you can test your configuration by following command:

```bash
./manage.py hermes_test
```

Command send message to all topics defined in settings to Hermes.
