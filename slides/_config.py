#!/usr/bin/env python
import logging
import os
import sys

from sliderepl import Deck


class SADeck(Deck):
    expose = Deck.expose + ('echo',)

    def __init__(self, path=None, echo_on=True, **options):
        Deck.__init__(self, path, **options)
        self.start_with_echo = echo_on

    def start(self):
        logging_config = {'format': '[SQL]: %(message)s',
                          'stream': self.highlight_stdout("sql")}
        logging.basicConfig(**logging_config)

        sys.path.insert(0, os.path.dirname(self.path))

        self._set_echo(self.start_with_echo and 'on' or 'off')

    def echo(self):
        """Toggle SQL echo on or off."""
        self._set_echo(not self._echo)

    def _set_echo(self, value):
        self._echo = value
        log = logging.getLogger('sqlalchemy.engine')
        if self._echo:
            log.setLevel(logging.INFO)
        else:
            log.setLevel(logging.WARN)
        print("%% SQL echo is now %s" % (self._echo and 'ON' or 'OFF'))

deck = SADeck
