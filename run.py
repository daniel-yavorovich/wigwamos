#!/usr/bin/env python
import logging
import time
import settings
from wwos import WigWamOS


def main(w):
    while True:
        stats = w.run()
        logging.info(
            'Stats: day {} / humidity {}% / temperature {}C / fan speed {}% / light brightness {}%'.format(
                stats[0], stats[1], stats[2], stats[3], stats[4]))
        time.sleep(settings.RUN_INTERVAL)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=settings.LOG_LEVEL)
    w = WigWamOS()
    main(w)
