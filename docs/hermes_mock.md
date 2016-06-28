# Hermes mock

Pyhermes provides simple mock of Hermes publisher. It could be useful for local
testing of interaction between services through Hermes events.

This mock is simple http server, which forwards every request it gets to the
subscriber (there could be only one subsriber, for now). Messages are proxied
with the same topic as received.

## Usage

### Obtaining the mock

To get the mock, either go to the `contrib` directory, or download it directly
from [github](https://github.com/allegro/pyhermes/tree/master/contrib/hermes_mock.py).

### Running

Type `python3 hermes_mock.py --help` for possible options:

```
$ python3 hermes_mock.py --help
usage: hermes_mock.py [-h] [-p PORT] -u PUBLISH_URL

Hermes mock server.

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port of Hermes mock server.
  -u PUBLISH_URL, --publish-url PUBLISH_URL
```

You could specify port, on which Hermes mock will be listening and URL of the
subscriber.
