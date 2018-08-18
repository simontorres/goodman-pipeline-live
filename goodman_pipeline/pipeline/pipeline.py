from __future__ import absolute_import

import argparse
import logging
import sys

from ..broadcaster import ZmqSubscriber


class MainApp(object):

    def __init__(self, args=None):
        if args is None:
            self.args = self._get_args()
        else:
            self.args = self._get_args(arguments=args)

        self.log = logging.getLogger(__name__)
        self._path = None
        self._subscriber = ZmqSubscriber(host=self.args.server,
                                         port=self.args.port)

    def __call__(self, *args, **kwargs):
        self.log.info("Pipeline started")

        for received  in self._subscriber.listen():
            print(received)


    @staticmethod
    def _get_args(arguments=None):
        parser = argparse.ArgumentParser(
            description="Watch for notifications and decide actions")
        # parser.add_argument('--path',
        #                     action='store',
        #                     default=os.getcwd(),
        #                     dest='path',
        #                     help="Path to directory to watch.")

        parser.add_argument('--server',
                            action='store',
                            default='localhost',
                            dest='server',
                            help='Server name or IP to subscribe to')

        parser.add_argument('--port',
                            action='store',
                            default='5556',
                            dest='port',
                            help='TCP/IP port to subscribe to')

        args = parser.parse_args(args=arguments)

        return args
