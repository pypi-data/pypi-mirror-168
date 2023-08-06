# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import unittest
import sys
import os

# -- We need to import for our parent folder here.
sys.path.append(os.path.join(sys.path[0], '..'))

from toybox.boxfile import Boxfile       # noqa: E402


class TestBoxfile(unittest.TestCase):
    """Unit tests for the Boxfile class."""

    def test_constructor(self):
        boxfile = Boxfile(os.path.join('tests', 'data', 'boxfile_old'))
        self.assertEqual(len(boxfile.urls()), 1)
        urls = boxfile.urls()
        self.assertEqual(len(urls), 1)
        url = urls[0]
        self.assertEqual(url.as_string, 'github.com/DidierMalenfant/pdbase')
        self.assertEqual(boxfile.versionsAsStringForUrl(url), '1')
        self.assertEqual(boxfile.maybeInstalledVersionAsStringForUrl(url), None)
        self.assertEqual(boxfile.maybeLuaImportFile(), None)

        boxfile = Boxfile(os.path.join('tests', 'data', 'boxfile_current'))
        self.assertEqual(len(boxfile.urls()), 1)
        urls = boxfile.urls()
        self.assertEqual(len(urls), 1)
        url = urls[0]
        self.assertEqual(urls[0].as_string, 'github.com/DidierMalenfant/pdbase')
        self.assertEqual(boxfile.versionsAsStringForUrl(url), '1')
        self.assertEqual(boxfile.maybeInstalledVersionAsStringForUrl(url), '1.2.3')
        self.assertEqual(boxfile.maybeLuaImportFile(), 'source/main.lua')

        folder = os.path.join('tests', 'data', 'boxfile_future')
        with self.assertRaises(SyntaxError) as context:
            Boxfile(folder)

        self.assertEqual(str(context.exception),
                         'Incorrect format for Boxfile \'' + os.path.join(folder, 'Boxfile') + '\'.\nMaybe you need to upgrade toybox?')

        folder = os.path.join('tests', 'data', 'boxfile_invalid')
        with self.assertRaises(SyntaxError) as context:
            Boxfile(folder)

        self.assertEqual(str(context.exception),
                         'Malformed JSON in Boxfile \'' + os.path.join(folder, 'Boxfile') + '\'.\nExpecting \',\' delimiter: line 3 column 5 (char 40).')


if __name__ == '__main__':
    unittest.main()
