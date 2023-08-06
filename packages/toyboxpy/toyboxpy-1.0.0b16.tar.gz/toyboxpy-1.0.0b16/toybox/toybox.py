# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import os
import getopt
import shutil

from pathlib import Path

from .__about__ import __version__
from .boxfile import Boxfile
from .exceptions import ArgumentError
from .version import Version
from .dependency import Dependency
from .git import Git
from .paths import Paths
from .utils import Utils
from .files import Files
from .url import Url


class Toybox:
    """A Lua, C and asset dependency manager for the Playdate SDK."""

    def __init__(self, args):
        """Initialise toybox based on user configuration."""

        self.box_file = None
        self.dependencies = []
        self.only_update = None
        self.installed_a_local_toybox = False

        try:
            # -- Gather the arguments
            opts, other_arguments = getopt.getopt(args, '')

            if len(other_arguments) == 0:
                raise SyntaxError('Expected a command! Maybe start with `toybox help`?')

            number_of_arguments = len(other_arguments)

            self.command = None
            self.argument = None
            self.second_argument = None

            i = 0
            argument = other_arguments[i]
            if len(argument):
                self.command = argument
            i += 1

            if i != number_of_arguments:
                argument = other_arguments[i]
                if len(argument):
                    self.argument = other_arguments[i]
                i += 1
                if i != number_of_arguments:
                    argument = other_arguments[i]
                    if len(argument):
                        self.second_argument = other_arguments[i]
                        i += 1

            if i != number_of_arguments:
                raise SyntaxError('Too many commands on command line.')

        except getopt.GetoptError:
            raise ArgumentError('Error reading arguments.')

    def main(self):
        switch = {
            'help': self.printUsage,
            'version': Toybox.printVersion,
            'info': self.printInfo,
            'add': self.addDependency,
            'remove': self.removeDependency,
            'update': self.update,
            'check': self.checkForUpdates,
            'set': self.set,
        }

        if self.command is None:
            print('No command found.\n')
            Toybox.printUsage()
            return

        method = switch.get(self.command)
        if method is None:
            raise ArgumentError('Unknow command \'' + self.command + '\'.')

        method()

        Toybox.checkForToyboxPyUpdates()

    def printUsage(self):
        method = None

        if self.argument is not None:
            switch = {
                'topics': Toybox.printTopics,
                'set': Toybox.printSetUsage
            }

            method = switch.get(self.argument)
            if method is None:
                raise ArgumentError('Error: Unknown topic \'' + self.argument + '\'.')

        Toybox.printVersion()
        print('Usage:')

        if method is not None:
            method()
            return

        print('    toybox help                 - Show a help message.')
        print('    toybox help <topic>         - Show a help message on a topic (use \'help topics\' for a list).')
        print('    toybox version              - Get the Toybox version.')
        print('    toybox info                 - Describe your dependency set.')
        print('    toybox add <url>            - Add a new dependency.')
        print('    toybox add <url> <version>  - Add a new dependency with a specific version.')
        print('    toybox remove <url>         - Remove a dependency.')
        print('    toybox update               - Update all the dependencies.')
        print('    toybox update <dependency>  - Update a single dependency.')
        print('    toybox check                - Check for updates.')
        print('    toybox set <name> <value>   - Set a configuration value for this toybox.')

    def printInfo(self, folder=None):
        if folder is None:
            print('Resolving dependencies...')
            self.box_file = box_file_for_folder = Boxfile(Paths.boxfileFolder())
        else:
            box_file_for_folder = Boxfile(folder)

        dependencies = Dependency.dependenciesForBoxfile(box_file_for_folder)
        if len(dependencies) == 0 and self.box_file == box_file_for_folder:
            print('Boxfile is empty.')
            return

        for dep in dependencies:
            info_string = '       - ' + str(dep) + ' -> '

            dep_folder = Paths.toyboxFolderFor(dep)
            dep_folder_exists = os.path.exists(dep_folder)

            version_installed_as_string = self.box_file.maybeInstalledVersionAsStringForUrl(dep.url)
            if dep_folder_exists and version_installed_as_string:
                info_string += version_installed_as_string
            elif dep_folder_exists:
                info_string += 'Unknown version.'
            else:
                info_string += 'Not installed.'

            print(info_string)

            if dep_folder_exists:
                self.printInfo(dep_folder)

    def checkForUpdates(self, folder=None):
        if folder is None:
            print('Resolving dependencies...')
            self.box_file = box_file_for_folder = Boxfile(Paths.boxfileFolder())
        else:
            box_file_for_folder = Boxfile(folder)

        dependencies = Dependency.dependenciesForBoxfile(box_file_for_folder)
        if len(dependencies) == 0 and self.box_file == box_file_for_folder:
            print('Boxfile is empty.')
            return

        something_needs_updating = False

        for dep in dependencies:
            version_available = dep.resolveVersion()
            if version_available is None:
                continue

            dep_folder = Paths.toyboxFolderFor(dep)
            if os.path.exists(dep_folder) is False:
                print('       - ' + str(dep) + ' -> Version ' + str(version_available) + ' is available.')
                something_needs_updating = True
                continue

            version_installed = None
            version_installed_as_string = self.box_file.maybeInstalledVersionAsStringForUrl(dep.url)
            if version_installed_as_string is None:
                print('       - ' + str(dep) + ' -> Version ' + str(version_available) + ' is available.')
                something_needs_updating = True
            else:
                version_installed = Version(version_installed_as_string)
                if version_installed != version_available:
                    if version_available.isLocal():
                        print('       - ' + str(dep) + ' -> Local version not installed.')
                    elif version_available.isBranch():
                        print('       - ' + str(dep) + ' -> A more recent commit is available.')
                    else:
                        print('       - ' + str(dep) + ' -> Version ' + str(version_available) + ' is available.')

                    something_needs_updating = True

            something_needs_updating |= self.checkForUpdates(dep_folder)

        if folder is None and something_needs_updating is False:
            print('You\'re all up to date!!')

        return something_needs_updating

    def addDependency(self):
        if self.argument is None:
            raise SyntaxError('Expected an argument to \'add\' command.')

        url = Url(self.argument)
        versions_as_string = self.second_argument

        new_dependency = Dependency(url)

        if versions_as_string is None:
            versions_as_string = new_dependency.git.getHeadBranch()

        new_dependency.replaceVersions(versions_as_string)

        versions_as_string = new_dependency.originalVersionsAsString()

        self.box_file = Boxfile(Paths.boxfileFolder())
        self.box_file.addDependencyWithURLAndVersions(url, versions_as_string)
        self.box_file.saveIfModified()

        print('Added a dependency for \'' + self.argument + '\' at \'' + versions_as_string + '\'.')

    def removeDependency(self):
        if self.argument is None:
            raise SyntaxError('Expected an argument to \'remove\' command.')

        url = Url(self.argument)

        self.box_file = Boxfile(Paths.boxfileFolder())
        self.box_file.removeDependencyWithURL(url)
        self.box_file.saveIfModified()

        dep = Dependency(url)
        dep.deleteFolderIn(Paths.toyboxesFolder())

        print('Removed a dependency for \'' + self.argument + '\'.')

    def set(self):
        if self.argument is None:
            raise ArgumentError('Expected a name argument to \'set\' command.')

        switch = {
            'lua_import': self.setLuaImport,
            'assets_sub_folder': self.setAssetsSubFolder,
        }

        if self.argument is None:
            raise ArgumentError('Expected a value to set for \'' + self.argument + '\'.')

        method = switch.get(self.argument)
        if method is None:
            raise ArgumentError('Unknown value \'' + self.argument + '\' for set command.')

        method()

    def setLuaImport(self):
        self.box_file = Boxfile(Paths.boxfileFolder())
        self.box_file.setLuaImport(self.second_argument)
        self.box_file.saveIfModified()

        print('Set Lua import file to \'' + self.second_argument + '\'.')

    def setAssetsSubFolder(self):
        self.box_file = Boxfile(Paths.boxfileFolder())
        self.box_file.setAssetsSubFolder(self.second_argument)
        self.box_file.saveIfModified()

        print('Set assets sub folder path to \'' + self.second_argument + '\'.')

    def installDependency(self, dep, no_copying=False):
        dependency_is_new = True

        for other_dep in self.dependencies:
            if other_dep.url == dep.url:
                other_dep.versions += dep.versions
                dep = other_dep
                dependency_is_new = False

        should_copy = (self.only_update is not None) and (self.only_update != dep.url.repo_name) and Toybox.toyboxExistsInBackup(dep)

        if (no_copying is False) and should_copy:
            print('Copying \'' + str(dep) + '.')
            self.copyToyboxFromBackup(dep)
            self.copyAssetsFromBackupIfAny(dep)
        else:
            version = dep.installIn(Paths.toyboxesFolder())
            if version is not None:
                installed_version_string = version.original_version

                if version.isBranch():
                    commit_hash = dep.git.getLatestCommitHashForBranch(version.original_version)
                    if commit_hash is None:
                        raise RuntimeError('Could not find latest commit hash for branch ' + version.original_version + '.')

                    installed_version_string += '@' + commit_hash
                else:

                    if version.isLocal():
                        self.installed_a_local_toybox = True

                info_string = 'Installed \'' + str(dep) + '\' -> ' + str(version)

                if should_copy and no_copying:
                    info_string += ' (force-installed by another dependency)'

                print(info_string + '.')

                self.box_file.setInstalledVersionStringForDependency(dep, installed_version_string)

            no_copying = True

            self.moveAssetsFromToyboxIfAny(dep)

        dep_box_file = dep.boxfile()
        for child_dep in Dependency.dependenciesForBoxfile(dep_box_file):
            self.installDependency(child_dep, no_copying)

        if dependency_is_new:
            self.dependencies.append(dep)

    def update(self):
        if self.argument is not None:
            self.only_update = self.argument

        Toybox.backupToyboxes()
        Toybox.backupAssets()

        try:
            self.box_file = Boxfile(Paths.boxfileFolder())
            for dep in Dependency.dependenciesForBoxfile(self.box_file):
                self.installDependency(dep)

            folder = Paths.toyboxesFolder()
            if os.path.exists(folder):
                Files.generateReadMeFileIn(folder)
                Files.generateLuaIncludeFile(self.dependencies)
                Files.generateMakefile(self.dependencies)
                Files.generateIncludeFile(self.dependencies)

            folder = Paths.assetsFolder()
            if os.path.exists(folder):
                Files.generateReadMeFileIn(folder)

            self.box_file.saveIfModified()

        except Exception:
            Toybox.restoreAssetsBackup()
            Toybox.restoreToyboxesBackup()
            raise

        Toybox.deleteToyboxesBackup()
        Toybox.deleteAssetsBackup()

        Files.restorePreCommitFileIfAny()

        if self.installed_a_local_toybox:
            Files.generatePreCommitFile()

        print('Finished.')

    @classmethod
    def printVersion(cls):
        print('🧸 toybox.py v' + __version__)

    @classmethod
    def printSetUsage(cls):
        print('    toybox set lua_import <value>        - Set the lua filename to import.')
        print('    toybox set assets_sub_folder <value> - Set the subfolder to use for assets.')

    @classmethod
    def printTopics(cls):
        print('    set     - List the names accepted bu the set command.')

    @classmethod
    def backupToyboxes(cls):
        Utils.backup(Paths.toyboxesFolder(), Paths.toyboxesBackupFolder())

    @classmethod
    def restoreToyboxesBackup(cls):
        Utils.restore(Paths.toyboxesBackupFolder(), Paths.toyboxesFolder())

    @classmethod
    def backupAssets(cls):
        Utils.backup(Paths.assetsFolder(), Paths.assetsBackupFolder())

    @classmethod
    def restoreAssetsBackup(cls):
        Utils.restore(Paths.assetsBackupFolder(), Paths.assetsFolder())

    @classmethod
    def toyboxExistsInBackup(cls, dep):
        return os.path.exists(Paths.toyboxBackupFolderFor(dep))

    @classmethod
    def copyToyboxFromBackup(cls, dep):
        source_path = Paths.toyboxBackupFolderFor(dep)
        if not os.path.exists(source_path):
            raise RuntimeError('Backup from ' + dep.subFolder() + ' cannot be found.')

        shutil.copytree(source_path, Paths.toyboxFolderFor(dep))

    @classmethod
    def copyAssetsFromBackupIfAny(cls, dep):
        source_path = Paths.assetsBackupFolderFor(dep)
        if os.path.exists(source_path):
            shutil.copytree(source_path, Paths.assetsFolderFor(dep))

    @classmethod
    def deleteToyboxesBackup(cls):
        Utils.delete(Paths.toyboxesBackupFolder())

    @classmethod
    def deleteAssetsBackup(cls):
        Utils.delete(Paths.assetsBackupFolder())

    @classmethod
    def moveAssetsFromToyboxIfAny(cls, dep):
        source_path = os.path.join(Paths.toyboxAssetsFolderFor(dep))
        if not os.path.exists(source_path):
            return

        dest_path = Paths.assetsFolderFor(dep)
        if os.path.exists(dest_path):
            raise RuntimeError('Something already installed assets in \'' + dest_path + '\'')

        os.makedirs(Path(dest_path).parent, exist_ok=True)

        shutil.move(source_path, dest_path)

    @classmethod
    def checkForToyboxPyUpdates(cls):
        try:
            latest_version = Git('https://github.com/toyboxpy/toybox.py').getLatestVersion()
            if latest_version is None:
                return

            if latest_version > Version(__version__):
                print('‼️  Version v' + str(latest_version) + ' is available for toybox.py. You have v' + __version__ + ' ‼️')
                print('Please run \'pip install toyboxpy --upgrade\' to upgrade.')
        except Exception:
            pass
