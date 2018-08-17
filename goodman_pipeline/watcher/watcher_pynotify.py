from __future__ import absolute_import

import argparse
import logging
import os
import pyinotify

from astropy.io.registry import IORegistryError
from ccdproc import CCDData


class EventHandler(pyinotify.ProcessEvent):

    def __init__(self):
        super(EventHandler, self).__init__()
        self.log = logging.getLogger(__name__)

    def process_IN_DELETE(self, event):
        self.log.info("File Deleted: {:s}".format(os.path.basename(event.pathname)))

    def process_IN_CREATE(self, event):
        print("File {:s} was created".format(event.pathname))

    def process_IN_CLOSE_WRITE(self, event):
        # print("This is what I want: {:s}.".format(event.pathname))
        message = "COMMAND {:s}".format(event.pathname)
        # publisher.broadcast(message=message)
        self._print_object(full_path=event.pathname)

    def _print_object(self, full_path):
        if ".fits" in full_path:
            try:
                ccd = CCDData.read(full_path, unit='adu')
                print(ccd.header['OBJECT'],
                      ccd.header['OBSTYPE'],
                      os.path.basename(full_path))
            except IORegistryError:
                self.log.warning("Unable to read file or is not a FITS file: "
                                 "{:s}".format(os.path.basename(full_path)))
        else:
            self.log.info("File Created: {:s}".format(os.path.basename(full_path)))


class FileSystemEventNotifier(object):

    def __init__(self):
        self.args = None
        self.log = logging.getLogger(__name__)
        self._file_events = pyinotify.IN_OPEN | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CLOSE_NOWRITE
        self._watch_manager = pyinotify.WatchManager()
        self._event_handler = EventHandler()
        self._notifier = pyinotify.Notifier(self._watch_manager,
                                            self._event_handler)

    def __call__(self, args=None):
        if args is None:
            self.args = self._get_args()
        else:
            self.args = self._get_args(arguments=args)

        self.log.info("Starting to monitor directory: {:s}".format(self.args.path))
        self._watch_manager.add_watch(self.args.path, self._file_events)

        self._notifier.loop()

    @staticmethod
    def _get_args(arguments=None):
        parser = argparse.ArgumentParser(
            description="Monitor a directory for new files and broadcast a "
                        "notification when this happens.")
        parser.add_argument('--path',
                            action='store',
                            default=os.getcwd(),
                            dest='path',
                            help="Path to directory to watch.")

        parser.add_argument('--server',
                            action='store',
                            default='*',
                            dest='server',
                            help='Range of IP to broadcast')

        parser.add_argument('--port',
                            action='store',
                            default='5556',
                            dest='port',
                            help='TCP/IP port to broadcast')

        args = parser.parse_args(args=arguments)

        return args

# from live_pipeline.zmq_communication_experiments.telemetry.core import \
#     ZmqPublisher

# publisher = ZmqPublisher("*", "5556")

# path = '/data/simon/Downloads/testing_watchdog'



if __name__ == '__main__':

    fsnotifier = FileSystemEventNotifier()

    fsnotifier()