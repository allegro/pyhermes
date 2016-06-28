#!/usr/bin/python3
"""
Simple mock of Hermes publisher, useful for local testing of communication
between services using Hermes events. Incoming message would be "proxied" to
publishing url with the same topic name.
"""

import argparse
import concurrent.futures
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen


SUCCESS_CODE = 201
TIMEOUT = 10  # in seconds
MAX_WORKERS = 2
MESSAGE_ID_HEADER = 'Hermes-Message-Id'
RETRY_COUNT_HEADER = 'Hermes-Retry-Count'

parser = argparse.ArgumentParser(description='Hermes mock server.')
parser.add_argument(
    '-p', '--port', dest='port', default=8888, type=int,
    help='Port of Hermes mock server.'
)
parser.add_argument('-u', '--publish-url', dest='publish_url', required=True)
args = parser.parse_args()


def _publish(path, data, msg_id):
    topic = path.split('/')[-1]
    url = args.publish_url + topic + '/'
    request = Request(
        url,
        data=data,
        headers={
            MESSAGE_ID_HEADER: msg_id,
            RETRY_COUNT_HEADER: 0,
        }
    )
    print('Publishing {} to {} (msg_id: {})'.format(data, url, msg_id))
    try:
        urlopen(request, timeout=TIMEOUT)
    except Exception as e:
        print('Exception during publishing data: {}'.format(e))


class HermesMockHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print('Get request on {}'.format(self.path))
        content_len = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(content_len)
        msg_id = str(uuid.uuid4())
        self.tp.submit(_publish, self.path, data, msg_id)
        self.send_response(SUCCESS_CODE)
        self.send_header(MESSAGE_ID_HEADER, msg_id)
        self.end_headers()
        return


def main():
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        handler = type('HermesHandler', (HermesMockHandler,), {'tp': executor})
        server = HTTPServer(('', args.port), handler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.socket.close()

if __name__ == '__main__':
    main()
