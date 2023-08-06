# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import os
import enum
import string

from semver import VersionInfo


class VersionIs(enum.Enum):
    """The possible outcomes of a comparison."""

    equal = 1
    less_than = 2
    less_than_or_equal = 3
    greater_than = 4
    greater_than_or_equal = 5


class VersionType(enum.Enum):
    """The different types of versions."""

    semver = 1
    branch = 2
    local = 3


class Version:
    """A helper class to compare dependency versions."""

    def __init__(self, version_as_string):
        """Create a version number from a string."""
        """Format can be simply a full semver version number (i.e. 3.2.5) to point to an exact version,"""
        """or a partial one (i.e. 3 or 3.2) to require any given major or minor version."""
        """It can also have a comparison operator as a prefix (i.e. '>3.0,2' or '<=3.4')."""

        self.operator = VersionIs.equal
        self.commit_hash = None
        self.asSemVer = None

        length = len(version_as_string)
        first_character = version_as_string[0]
        if length > 1:
            second_character = version_as_string[1]
        else:
            second_character = None

        if first_character == '/' or first_character == '~' or (second_character == ':' and first_character in string.ascii_letters):
            if first_character == '~':
                version_as_string = os.path.expanduser(version_as_string)

            self.original_version = version_as_string
            self.type = VersionType.local
        elif first_character == '>' or first_character == '<' or first_character in string.digits or (first_character == 'v' and second_character in string.digits):
            #  if first_character == 'v':
            #    first_character = version_as_string[1]

            self.original_version = version_as_string

            if first_character == '>':
                if version_as_string.startswith('>='):
                    self.operator = VersionIs.greater_than_or_equal
                    version_as_string = version_as_string[2:]
                else:
                    self.operator = VersionIs.greater_than
                    version_as_string = version_as_string[1:]
            elif first_character == '<':
                if version_as_string.startswith('<='):
                    self.operator = VersionIs.less_than_or_equal
                    version_as_string = version_as_string[2:]
                else:
                    self.operator = VersionIs.less_than
                    version_as_string = version_as_string[1:]

            if version_as_string[0] == 'v':
                version_as_string = version_as_string[1:]

            self.asSemVer = VersionInfo.parse(version_as_string)
            self.type = VersionType.semver
        else:
            components = version_as_string.split('@')
            if len(components) > 2:
                raise SyntaxError('Malformed branch version \'' + version_as_string + '\'.')

            if len(components) == 2:
                self.commit_hash = components[1]

            self.original_version = components[0]
            self.type = VersionType.branch

    def __eq__(self, other):
        if self.isBranch():
            return other.isBranch() and self.original_version == other.original_version and self.commit_hash == other.commit_hash
        elif self.isLocal():
            return other.isLocal() and self.original_version == other.original_version

        if other.asSemVer is None or self.asSemVer != other.asSemVer:
            return False

        if self.operator != other.operator:
            return False

        return True

    def __lt__(a, b):
        return a.asSemVer < b.asSemVer

    def __gt__(a, b):
        return a.asSemVer > b.asSemVer

    def __str__(self):
        if self.isLocal():
            version_string = self.original_version + '(local)'
        elif self.isBranch():
            version_string = self.original_version

            if self.commit_hash is not None:
                version_string += '@' + self.commit_hash

            version_string += '(branch)'
        else:
            switch = {
                VersionIs.equal: '',
                VersionIs.less_than: '<',
                VersionIs.less_than_or_equal: '<=',
                VersionIs.greater_than: '>',
                VersionIs.greater_than_or_equal: '>='
            }

            version_string = switch.get(self.operator) + str(self.asSemVer)

        return version_string

    def isBranch(self):
        return self.type == VersionType.branch

    def isLocal(self):
        return self.type == VersionType.local

    def includes(self, other):
        if other.operator != VersionIs.equal:
            raise SyntaxError('Right hand operand must be an exact version number, not a range.')

        other_is_branch = other.isBranch()
        other_is_local = other.isLocal()

        if self.operator is VersionIs.equal:
            self_is_branch = self.isBranch()
            if self_is_branch or other_is_branch:
                return self_is_branch == other_is_branch and self.original_version == other.original_version

            self_is_local = self.isLocal()
            if self_is_local or other_is_local:
                return self_is_local == other_is_local and self.original_version == other.original_version

            return other.asSemVer == self.asSemVer
        elif self.operator is VersionIs.less_than:
            return other_is_branch is False and other_is_local is False and other.asSemVer < self.asSemVer
        elif self.operator is VersionIs.less_than_or_equal:
            return other_is_branch is False and other_is_local is False and other.asSemVer <= self.asSemVer
        elif self.operator is VersionIs.greater_than:
            return other_is_branch is False and other_is_local is False and other.asSemVer > self.asSemVer
        else:
            return other_is_branch is False and other_is_local is False and other.asSemVer >= self.asSemVer

    def includedVersionsIn(self, list):
        result = []

        for version in list:
            if self.includes(version):
                result.append(version)

        return result

    @classmethod
    def maybeRangeFromIncompleteNumericVersion(cls, version_as_string):
        versions = []

        first_character = version_as_string[0]
        if first_character == '>' or first_character == '<':
            first_character = version_as_string[1]

            if first_character == '=':
                first_character = version_as_string[2]

        if (first_character < '0' or first_character > '9'):
            return [version_as_string]

        components = version_as_string.split('.')
        nb_of_components = len(components)
        if nb_of_components > 3:
            raise SyntaxError('Malformed version \'' + version_as_string + '\' (too many components).')

        nb_of_components_added = 0

        for i in range(nb_of_components, 3):
            # -- If we're missing any minor or patch numbers, we set them as 0.
            version_as_string += '.0'
            nb_of_components_added += 1

        if version_as_string.startswith('>') or version_as_string.startswith('<'):
            nb_of_components_added = 0

        if nb_of_components_added != 0:
            version_as_string = '>=' + version_as_string

        new_version = Version(version_as_string)
        versions.append(str(version_as_string))

        if nb_of_components_added == 1:
            top_bracket = new_version.asSemVer.bump_minor()
            top_bracket_as_string = '<' + str(top_bracket)
            versions.append(top_bracket_as_string)
        elif nb_of_components_added == 2:
            top_bracket = new_version.asSemVer.bump_major()
            top_bracket_as_string = '<' + str(top_bracket)
            versions.append(top_bracket_as_string)

        return versions
