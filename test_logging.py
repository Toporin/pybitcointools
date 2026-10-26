import ast
import contextlib
import io
import logging
import pathlib
import unittest

import pycryptotools
import pycryptotools.coins  # noqa: F401 -- registers the coin/explorer loggers
from pycryptotools.mnemonic import words_verify

# to run test: python3 -m unittest test_logging

PKG_DIR = pathlib.Path(pycryptotools.__file__).parent


class TestLogConfiguration(unittest.TestCase):
    """Level and handler policy belong to the application, not the library."""

    def setUp(self):
        self.pkg_logger = logging.getLogger('pycryptotools')
        self._saved_level = self.pkg_logger.level

    def tearDown(self):
        self.pkg_logger.setLevel(self._saved_level)

    def _module_loggers(self):
        return [logger for name, logger in logging.Logger.manager.loggerDict.items()
                if name.startswith('pycryptotools.') and isinstance(logger, logging.Logger)]

    def test_package_has_a_null_handler(self):
        """Without one, records fall through to logging.lastResort (stderr)."""
        self.assertTrue(any(isinstance(h, logging.NullHandler) for h in self.pkg_logger.handlers))

    def test_module_loggers_stay_at_notset(self):
        """A module logger with its own level would block the cascade."""
        loggers = self._module_loggers()
        self.assertTrue(loggers)
        for logger in loggers:
            with self.subTest(logger=logger.name):
                self.assertEqual(logger.level, logging.NOTSET)
                self.assertFalse(logger.handlers)

    def test_set_log_level_cascades_to_every_module(self):
        for level in (logging.DEBUG, logging.ERROR):
            pycryptotools.set_log_level(level)
            for logger in self._module_loggers():
                with self.subTest(logger=logger.name, level=level):
                    self.assertEqual(logger.getEffectiveLevel(), level)


class TestNoLeak(unittest.TestCase):

    def test_library_does_not_print(self):
        """Library output must go through logging, never stdout."""
        offenders = []
        for path in PKG_DIR.rglob('*.py'):
            tree = ast.parse(path.read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id == 'print'):
                    offenders.append(f"{path.relative_to(PKG_DIR)}:{node.lineno}")
        self.assertEqual(offenders, [], "print() calls in library:\n" + "\n".join(offenders))

    def test_mnemonic_checksum_does_not_expose_entropy(self):
        """words_verify() used to print the raw entropy of the mnemonic."""
        words = "tonight stem cause eyebrow estate smart duck wrong toe under job danger"
        stdout = io.StringIO()
        with self.assertLogs('pycryptotools', level=logging.DEBUG) as logs, \
                contextlib.redirect_stdout(stdout):
            logging.getLogger('pycryptotools').debug("sentinel")  # assertLogs needs one record
            words_verify(words.split())  # result irrelevant: we only check nothing leaks
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(logs.output, ["DEBUG:pycryptotools:sentinel"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
