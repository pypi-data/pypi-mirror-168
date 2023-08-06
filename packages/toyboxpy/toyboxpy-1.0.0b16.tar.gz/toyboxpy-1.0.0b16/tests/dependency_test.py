# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import unittest
import sys
import os

# -- We need to import for our parent folder here.
sys.path.append(os.path.join(sys.path[0], '..'))

from toybox.dependency import Dependency       # noqa: E402
from toybox.dependency import DependencyError  # noqa: E402
from toybox.version import Version  # noqa: E402
from toybox.url import Url  # noqa: E402


class MockGit:
    """Mock of a Git class for the purpose of testing the Dependency class."""

    def __init__(self, tags, branches=[]):
        """Setup access to the git repo at url."""
        self.tags = tags
        self.branches = branches

    def listTags(self):
        return self.tags

    def listTagVersions(self):
        # -- In our case we can use the same data as long as all tags passed to MockGit are version tags.
        tag_versions = []
        for tag in self.listTags():
            tag_versions.append(Version(tag))

        return tag_versions

    def listBranches(self):
        return self.branches

    def isATag(self, name):
        return name in self.tags

    def isABranch(self, name):
        return name in self.branches

    def getLatestCommitHashForBranch(self, branch):
        return 'aaf867d2725ab51a770b036c219e1cfb676e79b7'


class TestDependency(unittest.TestCase):
    """Unit tests for the Dependency class."""

    def test_addVersions(self):
        dependency = TestDependency.dependencyObject()
        dependency.addVersions('develop')
        self.assertEqual(len(dependency.versions), 1)
        self.assertTrue(dependency.versions[0].isBranch())
        self.assertEqual(dependency.versions[0].original_version, 'develop')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('>1.0 <3 <2.5')
        self.assertEqual(len(dependency.versions), 3)
        self.assertEqual(dependency.versions[0].original_version, '>1.0.0')
        self.assertEqual(dependency.versions[1].original_version, '<3.0.0')
        self.assertEqual(dependency.versions[2].original_version, '<2.5.0')

        folder = '/' + os.path.join('My', 'Local', 'Folder')
        dependency = TestDependency.dependencyObject()
        dependency.addVersions(folder)
        self.assertEqual(len(dependency.versions), 1)
        self.assertTrue(dependency.versions[0].isLocal())
        self.assertEqual(dependency.versions[0].original_version, folder)

        folder = os.path.join('J:', 'My', 'Local', 'Folder')
        dependency = TestDependency.dependencyObject()
        dependency.addVersions(folder)
        self.assertEqual(len(dependency.versions), 1)
        self.assertTrue(dependency.versions[0].isLocal())
        self.assertEqual(dependency.versions[0].original_version, folder)

        dependency = TestDependency.dependencyObject()
        with self.assertRaises(SyntaxError):
            dependency.addVersions('>1 <=4.5 >4 <6')

    def test_resolveVersion(self):
        dependency = TestDependency.dependencyObject()
        dependency.addVersions('>v1.2.3')
        self.assertEqual(dependency.resolveVersion().original_version, 'v3.2.3')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('3')
        self.assertEqual(dependency.resolveVersion().original_version, 'v3.2.3')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('<2.0.0')
        self.assertEqual(dependency.resolveVersion().original_version, 'v1.0.2')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('1.0')
        self.assertEqual(dependency.resolveVersion().original_version, 'v1.0.2')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('>v1.0.0 <2.0.0')
        self.assertEqual(dependency.resolveVersion().original_version, 'v1.0.2')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('>v1.0.0 <=2.0.0')
        self.assertEqual(dependency.resolveVersion().original_version, 'v2.0.0')

        dependency = TestDependency.dependencyObject()
        with self.assertRaises(DependencyError):
            dependency.resolveVersion()

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('main')
        self.assertEqual(dependency.resolveVersion().original_version, 'main')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('test')
        with self.assertRaises(DependencyError):
            dependency.resolveVersion()

        folder = '/' + os.path.join('My', 'Test', 'Folder')
        dependency = TestDependency.dependencyObject()
        dependency.addVersions(folder)
        self.assertEqual(dependency.resolveVersion().original_version, folder)

        folder = os.path.join('F:', 'My', 'Test', 'Folder')
        dependency = TestDependency.dependencyObject()
        dependency.addVersions(folder)
        self.assertEqual(dependency.resolveVersion().original_version, folder)

    @classmethod
    def dependencyObject(cls):
        dependency = Dependency(Url('toyboxpy.io/DidierMalenfant/MyProject.py'))
        dependency.git = MockGit(['v1.0.0', 'v1.0.2', 'v2.0.0', 'v2.1.0', 'v3.0.0', 'v3.2.3'],
                                 {'main': 'aaf867d2725ab51a770b036c219e1cfb676e79b7', 'develop': '10167a78efd194d4984c3e670bec38b8ccaf97eb'})
        return dependency


if __name__ == '__main__':
    unittest.main()
