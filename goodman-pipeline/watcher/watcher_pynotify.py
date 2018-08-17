from __future__ import absolute_import

import os

import pyinotify
from ccdproc import CCDData


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_DELETE(self, event):
        pass

    def process_IN_CREATE(self, event):
        print("File {:s} was created".format(event.pathname))

    def process_IN_CLOSE_WRITE(self, event):
        # print("This is what I want: {:s}.".format(event.pathname))
        message = "COMMAND {:s}".format(event.pathname)
        # publisher.broadcast(message=message)
        self._print_object(full_path=event.pathname)

    def _print_object(self, full_path):
        ccd = CCDData.read(full_path, unit='adu')
        print(ccd.header['OBJECT'], ccd.header['OBSTYPE'], os.path.basename(full_path))


class FileSystemEventNotifier(object):

    def __init__(self):
        self.args = None
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
        self._watch_manager.add_watch(self.args.path, self._file_events)

        self._notifier.loop()

    def _get_args(self, arguments=None):
        return None

# from live_pipeline.zmq_communication_experiments.telemetry.core import \
#     ZmqPublisher

# publisher = ZmqPublisher("*", "5556")

# path = '/data/simon/Downloads/testing_watchdog'



if __name__ == '__main__':

    fsnotifier = FileSystemEventNotifier()

    fsnotifier()