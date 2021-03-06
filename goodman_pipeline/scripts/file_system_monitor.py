from __future__ import absolute_import

from goodman_pipeline.watcher import FileSystemEventNotifier
import logging

log_format = '[%(asctime)s][%(levelname).1s]: %(message)s'
date_format = '%H:%M:%S'

if __name__ == '__main__':
    log_formatter = logging.Formatter(fmt=log_format,
                                      datefmt=date_format)
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        datefmt=date_format)
    log = logging.getLogger(__name__)

    fs_notify = FileSystemEventNotifier()

    fs_notify()