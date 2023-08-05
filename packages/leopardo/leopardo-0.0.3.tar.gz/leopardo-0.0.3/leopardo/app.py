# -----------------------------------------------------------------------------
# leopardo [Configurable fast-access toolset]
# (C) 2022 A. Shavykin <0.delameter@gmail.com>
# -----------------------------------------------------------------------------
"""
SYNOPSIS
    leopardo
    leopardo --help

Prints out this help or crashes with NotImplementedError.

ARGUMENTS
  No.
"""
import sys

from pytermor import Styles


# noinspection PyMethodMayBeStatic
class App:
    def run(self):
        try:
            self._entrypoint()
        except Exception as e:
            self._print_exception(e)
            self._exit(1)
        self._exit(0)

    def _entrypoint(self):
        if {'-h', '--help'}.intersection(sys.argv):
            self._print_usage()
            return

        self._parse_args()
        raise NotImplementedError

    def _parse_args(self):
        pass

    def _print_usage(self):
        print(__doc__)

    def _print_error(self):
        print(Styles.ERROR.render('[ERR]'))

    def _print_exception(self, e):
        print(str(e), file=sys.stderr)

    def _exit(self, code: int):
        print()
        exit(code)


if __name__ == '__main__':
    App().run()
