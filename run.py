#!/usr/bin/env python
import logging
import time
import settings
from wwos import WigWamOS


def main(w):
    while True:
        logging.info('Starting...')
        w.run()
        time.sleep(settings.RUN_INTERVAL)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=settings.LOG_LEVEL)
    w = WigWamOS()
    main(w)
