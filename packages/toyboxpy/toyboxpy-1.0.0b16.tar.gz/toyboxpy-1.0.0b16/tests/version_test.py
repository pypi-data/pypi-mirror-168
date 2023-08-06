# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import unittest
import sys
import os

# -- We need to import for our parent folder here.
sys.path.append(os.path.join(sys.path[0], '..'))

from toybox.version import Version       # noqa: E402
from toybox.version import VersionIs     # noqa: E402


class TestVersion(unittest.TestCase):
    """Unit tests for the Version class."""

    def test_Version(self):
        with self.assertRaises(ValueError):
            Version('34.2')

        version = Version('0.0.0')
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(version.asSemVer.major, 0)
        self.assertEqual(version.asSemVer.minor, 0)
        self.assertEqual(version.asSemVer.patch, 0)
        self.assertEqual(str(version), '0.0.0')
        self.assertEqual(version.original_version, '0.0.0')
        self.assertFalse(version.isBranch())

        version = Version('5.12.4')
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '5.12.4')
        self.assertEqual(version.original_version, '5.12.4')
        self.assertFalse(version.isBranch())

        version = Version('v5.12.4')
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '5.12.4')
        self.assertEqual(version.original_version, 'v5.12.4')
        self.assertFalse(version.isBranch())

        version = Version('>5.12.4')
        self.assertEqual(version.operator, VersionIs.greater_than)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '>5.12.4')
        self.assertEqual(version.original_version, '>5.12.4')
        self.assertFalse(version.isBranch())

        version = Version('>v5.12.4')
        self.assertEqual(version.operator, VersionIs.greater_than)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '>5.12.4')
        self.assertEqual(version.original_version, '>v5.12.4')
        self.assertFalse(version.isBranch())

        version = Version('>=5.12.4')
        self.assertEqual(version.operator, VersionIs.greater_than_or_equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '>=5.12.4')
        self.assertEqual(version.original_version, '>=5.12.4')
        self.assertFalse(version.isBranch())

        version = Version('>=v5.12.4')
        self.assertEqual(version.operator, VersionIs.greater_than_or_equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '>=5.12.4')
        self.assertEqual(version.original_version, '>=v5.12.4')
        self.assertFalse(version.isBranch())

        version = Version('<5.12.4')
        self.assertEqual(version.operator, VersionIs.less_than)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '<5.12.4')
        self.assertEqual(version.original_version, '<5.12.4')
        self.assertFalse(version.isBranch())

        version = Version('<v5.12.4')
        self.assertEqual(version.operator, VersionIs.less_than)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '<5.12.4')
        self.assertEqual(version.original_version, '<v5.12.4')
        self.assertFalse(version.isBranch())

        version = Version('<=5.12.4')
        self.assertEqual(version.operator, VersionIs.less_than_or_equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '<=5.12.4')
        self.assertEqual(version.original_version, '<=5.12.4')
        self.assertFalse(version.isBranch())

        version = Version('<=v5.12.4')
        self.assertEqual(version.operator, VersionIs.less_than_or_equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '<=5.12.4')
        self.assertEqual(version.original_version, '<=v5.12.4')
        self.assertFalse(version.isBranch())

        version = Version('main@aaf867d2725ab51a770b036c219e1cfb676e79b7')
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(str(version), 'main@aaf867d2725ab51a770b036c219e1cfb676e79b7(branch)')
        self.assertEqual(version.original_version, 'main')
        self.assertTrue(version.isBranch())

        version = Version('very')
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(str(version), 'very(branch)')
        self.assertEqual(version.original_version, 'very')
        self.assertTrue(version.isBranch())

        folder = '/' + os.path.join('This', 'Is', 'My', 'Folder')
        version = Version(folder)
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(str(version), folder + '(local)')
        self.assertEqual(version.original_version, folder)
        self.assertTrue(version.isLocal())

        folder = os.path.join('C:', 'This', 'Is', 'My', 'Folder')
        version = Version(folder)
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(str(version), folder + '(local)')
        self.assertEqual(version.original_version, folder)
        self.assertTrue(version.isLocal())

        rel_path = os.path.join('~', 'This', 'Is', 'My', 'Folder')
        full_path = os.path.expanduser(rel_path)
        version = Version(rel_path)
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(str(version), full_path + '(local)')
        self.assertEqual(version.original_version, full_path)
        self.assertTrue(version.isLocal())

    def test_operatorEqual(self):
        self.assertTrue(Version('5.12.4') == Version('5.12.4'))
        self.assertTrue(Version('<5.12.4') == Version('<5.12.4'))
        self.assertTrue(Version('<=5.12.4') == Version('<=5.12.4'))
        self.assertTrue(Version('>5.12.4') == Version('>5.12.4'))
        self.assertTrue(Version('>=5.12.4') == Version('>=5.12.4'))

        self.assertFalse(Version('5.12.4') == Version('5.13.4'))
        self.assertFalse(Version('>=5.12.4') == Version('<5.13.4'))
        self.assertFalse(Version('5.12.4') == Version('>5.12.4'))
        self.assertFalse(Version('>=5.12.4') == Version('5.12.4'))

        self.assertFalse(Version('toto') == Version('main'))
        folder = '/' + os.path.join('This', 'Is', 'My', 'Folder')
        self.assertFalse(Version(folder) == Version('main'))
        folder2 = '/' + os.path.join('This', 'Is', 'My', 'Other')
        self.assertFalse(Version(folder) == Version(folder2))

        folder = 'C:' + os.path.join('This', 'Is', 'My', 'Folder')
        self.assertFalse(Version(folder) == Version('main'))
        folder2 = 'C:' + os.path.join('This', 'Is', 'My', 'Other')
        self.assertFalse(Version(folder) == Version(folder2))

    def test_maybeRangeFromIncompleteNumericVersion(self):
        versions = Version.maybeRangeFromIncompleteNumericVersion('3.4.2')
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0], '3.4.2')

        versions = Version.maybeRangeFromIncompleteNumericVersion('2')
        self.assertEqual(len(versions), 2)
        self.assertEqual(versions[0], '>=2.0.0')
        self.assertEqual(versions[1], '<3.0.0')

        versions = Version.maybeRangeFromIncompleteNumericVersion('1.4')
        self.assertEqual(len(versions), 2)
        self.assertEqual(versions[0], '>=1.4.0')
        self.assertEqual(versions[1], '<1.5.0')

        versions = Version.maybeRangeFromIncompleteNumericVersion('>10.2.9')
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0], '>10.2.9')

        versions = Version.maybeRangeFromIncompleteNumericVersion('<=5.5')
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0], '<=5.5.0')

        versions = Version.maybeRangeFromIncompleteNumericVersion('develop')
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0], 'develop')

        folder = '/' + os.path.join('This', 'Is', 'My', 'Folder')
        versions = Version.maybeRangeFromIncompleteNumericVersion(folder)
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0], folder)

        folder = os.path.join('d:', 'This', 'Is', 'My', 'Folder')
        versions = Version.maybeRangeFromIncompleteNumericVersion(folder)
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0], folder)

        with self.assertRaises(ValueError):
            Version.maybeRangeFromIncompleteNumericVersion('<3.4.2 >3 <5')

    def test_includes(self):
        with self.assertRaises(SyntaxError):
            Version('<3.4.2').includes(Version('>3.4.2'))

        self.assertTrue(Version('3.4.2').includes(Version('3.4.2')))
        self.assertFalse(Version('3.4.2').includes(Version('3.40.2')))

        self.assertTrue(Version('>3.4.2').includes(Version('3.40.2')))
        self.assertFalse(Version('>3.4.2').includes(Version('3.3.2')))

        self.assertTrue(Version('<3.4.2').includes(Version('3.3.2')))
        self.assertFalse(Version('<3.4.2').includes(Version('3.4.2')))

        self.assertTrue(Version('>=3.4.2').includes(Version('3.4.2')))
        self.assertTrue(Version('>=3.4.2').includes(Version('3.40.2')))
        self.assertFalse(Version('>=3.4.2').includes(Version('3.3.2')))

        self.assertTrue(Version('<=3.4.2').includes(Version('3.4.2')))
        self.assertTrue(Version('<=3.4.2').includes(Version('3.3.2')))
        self.assertFalse(Version('<=3.4.2').includes(Version('5.4.1')))

        self.assertTrue(Version('main').includes(Version('main')))
        self.assertFalse(Version('main').includes(Version('test')))
        self.assertFalse(Version('main').includes(Version('3.4.2')))

        folder = '/' + os.path.join('This', 'Is', 'My', 'Folder')
        self.assertTrue(Version(folder).includes(Version(folder)))
        folder2 = '/' + os.path.join('This', 'Is', 'My', 'Other')
        self.assertFalse(Version(folder).includes(Version(folder2)))
        self.assertFalse(Version(folder).includes(Version('3.4.2')))

        folder = os.path.join('z:', 'This', 'Is', 'My', 'Folder')
        self.assertTrue(Version(folder).includes(Version(folder)))
        folder2 = os.path.join('D:', 'This', 'Is', 'My', 'Other')
        self.assertFalse(Version(folder).includes(Version(folder2)))
        self.assertFalse(Version(folder).includes(Version('3.4.2')))

    def test_includedVersionsIn(self):
        self.assertEqual(Version('<5.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [Version('3.2.1'), Version('4.2.1')])

        self.assertEqual(Version('<3.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [])

        self.assertEqual(Version('<=5.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [Version('3.2.1'), Version('4.2.1'), Version('5.0.0')])

        self.assertEqual(Version('<=2.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [])

        self.assertEqual(Version('4.2.1').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [Version('4.2.1')])

        self.assertEqual(Version('4.3.1').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [])

        self.assertEqual(Version('>4.3.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [Version('5.0.0'), Version('5.2.1')])

        self.assertEqual(Version('>6.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [])

        self.assertEqual(Version('>=5.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [Version('5.0.0'), Version('5.2.1')])

        self.assertEqual(Version('>=5.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [])

        branchVersion = Version('develop')
        self.assertEqual(branchVersion.includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), branchVersion]),
                         [branchVersion])
        self.assertEqual(Version('5.2.1').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), branchVersion]),
                         [Version('5.2.1')])
        self.assertEqual(Version('>=4.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), branchVersion]),
                         [Version('5.0.0'), Version('5.2.1')])
        self.assertEqual(Version('<5.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), branchVersion]),
                         [Version('3.2.1'), Version('4.2.1')])
        self.assertEqual(Version('<6.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), branchVersion]),
                         [Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')])

        localVersion = Version('/' + os.path.join('This', 'Is', 'My', 'Folder'))
        self.assertEqual(localVersion.includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), localVersion]),
                         [localVersion])
        self.assertEqual(Version('5.2.1').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), localVersion]),
                         [Version('5.2.1')])
        self.assertEqual(Version('>=4.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), localVersion]),
                         [Version('5.0.0'), Version('5.2.1')])
        self.assertEqual(Version('<5.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), localVersion]),
                         [Version('3.2.1'), Version('4.2.1')])
        self.assertEqual(Version('<6.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), localVersion]),
                         [Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')])

        localVersion = Version(os.path.join('S:', 'This', 'Is', 'My', 'Folder'))
        self.assertEqual(localVersion.includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), localVersion]),
                         [localVersion])
        self.assertEqual(Version('5.2.1').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), localVersion]),
                         [Version('5.2.1')])
        self.assertEqual(Version('>=4.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), localVersion]),
                         [Version('5.0.0'), Version('5.2.1')])
        self.assertEqual(Version('<5.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), localVersion]),
                         [Version('3.2.1'), Version('4.2.1')])
        self.assertEqual(Version('<6.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), localVersion]),
                         [Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')])


if __name__ == '__main__':
    unittest.main()
