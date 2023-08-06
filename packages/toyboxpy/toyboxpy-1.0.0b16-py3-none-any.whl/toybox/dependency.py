# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import os
import shutil
import platform

from .git import Git
from .version import Version
from .exceptions import DependencyError
from .boxfile import Boxfile
from .paths import Paths


class Dependency:
    """A helper class for toybox dependencies."""

    def __init__(self, url):
        """Create a dependency given a URL and a tag or branch."""

        self.url = url

        self.git = Git('https://' + self.url.as_string + '.git')

        self.versions = []
        self.last_version_installed = None
        self.box_file = None

    def __str__(self):
        string_version = self.url.as_string + '@'

        if len(self.versions) > 1:
            string_version += '('

        separator = ''
        for version in self.versions:
            string_version += separator + version.original_version
            separator = ' '

        if len(self.versions) > 1:
            string_version += ')'

        return string_version

    def subFolder(self):
        return os.path.join(self.url.server, self.url.username, self.url.repo_name)

    def boxfile(self):
        if self.box_file is None:
            self.box_file = Boxfile(Paths.toyboxFolderFor(self))

        return self.box_file

    def resolveVersion(self):
        branch = None
        versions = None

        try:
            for version in self.versions:
                if version.isLocal():
                    return version
                elif version.isBranch():
                    if branch is not None:
                        raise DependencyError

                    if self.git.isABranch(version.original_version):
                        commit_hash = self.git.getLatestCommitHashForBranch(version.original_version)
                        if commit_hash is None:
                            raise DependencyError

                        branch = Version(version.original_version + '@' + commit_hash)
                else:
                    if branch is not None:
                        raise DependencyError

                    if versions is None:
                        versions = self.git.listTagVersions()

                    versions = version.includedVersionsIn(versions)

            if branch is not None:
                return branch
            elif versions is None:
                raise DependencyError
            else:
                if len(versions) > 0:
                    return versions[-1]
                else:
                    raise DependencyError
        except DependencyError:
            raise DependencyError('Can\'t resolve version with \'' + self.originalVersionsAsString() + '\' for \'' + self.url.as_string + '\'.')

    def replaceVersions(self, versions_as_string):
        self.versions = []
        self.addVersions(versions_as_string)

    def addVersions(self, versions_as_string):
        separated_versions = versions_as_string.split(' ')
        if len(separated_versions) > 3:
            raise SyntaxError('Malformed version string \'' + versions_as_string + '\'. Too many versions.')

        for version_as_string in separated_versions:
            if len(version_as_string) == 0:
                continue

            for version in Version.maybeRangeFromIncompleteNumericVersion(version_as_string):
                self.versions.append(Version(version))

    def isATag(self, name):
        return self.git.isATag(name)

    def isABranch(self, name):
        return self.git.isABranch(name)

    def originalVersionsAsString(self):
        versions_as_string = ''

        for version in self.versions:
            if len(versions_as_string) != 0:
                versions_as_string += ' '

            versions_as_string += version.original_version

        return versions_as_string

    def installIn(self, toyboxes_folder):
        version_resolved = self.resolveVersion()

        if version_resolved is None:
            raise DependencyError('Can\'t resolve version with \'' + self.originalVersionsAsString() + '\' for \'' + self.url.as_string + '\'.')

        if self.last_version_installed is not None and self.last_version_installed.original_version == version_resolved.original_version:
            return

        folder = os.path.join(toyboxes_folder, self.subFolder())

        if os.path.exists(folder):
            shutil.rmtree(folder)

        if version_resolved.isLocal():
            system_name = platform.system()
            if system_name == 'Darwin' or system_name == 'Linux':
                # -- On macOs and Linux we can use softlinks to point to a local version of a toybox.
                self.softlinkFromTo(version_resolved.original_version, folder)
            else:
                self.copyFromTo(version_resolved.original_version, folder)
        else:
            os.makedirs(folder, exist_ok=True)

            self.git.cloneIn(version_resolved.original_version, folder)

        dependency_git_folder = os.path.join(folder, '.git')
        if os.path.exists(dependency_git_folder):
            shutil.rmtree(dependency_git_folder)

        self.last_version_installed = version_resolved

        return version_resolved

    def softlinkFromTo(self, source, dest):
        if not os.path.exists(source):
            raise RuntimeError('Local toybox folder ' + source + ' cannot be found.')

        os.makedirs(dest, exist_ok=True)

        for file_or_dir in os.listdir(source):
            if file_or_dir[0] == '.':
                continue

            os.symlink(os.path.join(source, file_or_dir), os.path.join(dest, file_or_dir))

    def copyFromTo(self, source, dest):
        if not os.path.exists(source):
            raise RuntimeError('Local toybox folder ' + source + ' cannot be found.')

        shutil.copytree(source, os.path.join(dest, ''))

    def deleteFolderIn(self, toyboxes_folder):
        folder = os.path.join(toyboxes_folder, self.subFolder())

        if os.path.exists(folder):
            shutil.rmtree(folder)

    @classmethod
    def dependenciesForBoxfile(cls, box_file):
        deps = []

        for url in box_file.urls():
            dep = Dependency(url)
            dep.addVersions(box_file.versionsAsStringForUrl(url))
            deps.append(dep)

        return deps
