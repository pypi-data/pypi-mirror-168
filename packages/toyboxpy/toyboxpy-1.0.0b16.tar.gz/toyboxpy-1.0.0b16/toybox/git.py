# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import subprocess

from .version import Version


class Git:
    """Utility methods for git repos."""

    def __init__(self, url_as_string):
        """Setup access to the git repo at url."""

        self.url_as_string = url_as_string
        self.refs = None
        self.tags = None
        self.tag_versions = None
        self.branches = None
        self.head_branch = None
        self.latest_version = None

    def git(self, arguments, folder=None):
        commands = ['git'] + arguments.split()
        commands.append(self.url_as_string)

        if folder is not None:
            commands.append(folder)

        try:
            process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                if str(stdout).startswith('b"usage: git'):
                    # -- git is giving us the usage info back it seems.
                    raise SyntaxError('Invalid git command line')
                else:
                    error = str(stderr)[2:-1]
                    if error.startswith('fatal: not a git repository (or any of the parent directories): .git'):
                        raise RuntimeError('Error: Your project folder needs to be a git repo for certain commands to work correctly.')

                    # -- Or maybe something else went wrong.
                    raise RuntimeError('Error running git: ' + error.split('\\n')[0])

            # -- Output is bracketed with b'' when converted from bytes.
            return str(stdout)[2:-1]
        except RuntimeError:
            raise
        except SyntaxError:
            raise
        except Exception as e:
            raise RuntimeError('Error running git: ' + str(e))

    def listRefs(self):
        if self.refs is None:
            self.refs = {}
            for ref in self.git('ls-remote --refs').split('\\n'):
                refs_index = ref.find('refs/')
                if refs_index >= 0:
                    self.refs[ref[refs_index + 5:]] = ref[:40]

        return self.refs

    def listBranches(self):
        if self.branches is None:
            self.branches = {}
            refs = self.listRefs()
            for ref in refs.keys():
                if ref.startswith('heads/'):
                    self.branches[ref[6:]] = refs[ref]

        return self.branches

    def getHeadBranch(self):
        if self.head_branch is None:
            for line in self.git('remote show').split('\\n'):
                if line.startswith('  HEAD branch:'):
                    self.head_branch = line[15:]

            if self.head_branch is None:
                raise RuntimeError('Cannot find head branch for \'' + self.url_as_string + '\'.')

        return self.head_branch

    def listTags(self):
        if self.tags is None:
            self.tags = []
            for ref in self.listRefs().keys():
                if ref.startswith('tags/'):
                    tag = ref[5:]
                    if not tag.startswith('@'):
                        self.tags.append(tag)

        return self.tags

    def listTagVersions(self):
        if self.tag_versions is None:
            self.tag_versions = []

            for tag in self.listTags():
                try:
                    self.tag_versions.append(Version(tag))
                except ValueError:
                    pass

            self.tag_versions = sorted(self.tag_versions)

        return self.tag_versions

    def getLatestVersion(self):
        if self.latest_version is None:
            all_versions = self.listTagVersions()

            if len(all_versions) > 0:
                self.latest_version = all_versions[-1]

        return self.latest_version

    def getLatestCommitHashForBranch(self, branch_name):
        return self.listBranches().get(branch_name)

    def isABranch(self, name):
        return name in self.listBranches()

    def isATag(self, name):
        for tag in self.listTags():
            if tag == name:
                return True

        return False

    def cloneIn(self, tag, folder):
        self.git('clone --quiet --depth 1 --branch ' + tag, folder)
