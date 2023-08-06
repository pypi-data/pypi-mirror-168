# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import json
import os

from .url import Url


class Boxfile:
    """Read and parse a toybox config file."""

    def __init__(self, boxfile_folder):
        """Read the Boxfile for the current folder."""

        self.boxfile_path = os.path.join(boxfile_folder, 'Boxfile')

        self.json_content = {}
        self.json_toyboxes = None
        self.json_config = None
        self.json_installed = None
        self.url_to_string = None
        self.was_modified = False

        if not os.path.exists(self.boxfile_path):
            # -- If we can't find it we may still create it later.
            return

        try:
            with open(self.boxfile_path, 'r') as file:
                self.json_content = json.load(file)
        except Exception as e:
            raise SyntaxError('Malformed JSON in Boxfile \'' + self.boxfile_path + '\'.\n' + str(e) + '.')

        self.was_modified = Boxfile.maybeConvertOldBoxfile(self.json_content)

        for key in self.json_content.keys():
            value = self.json_content[key]
            value_type = type(value).__name__

            if value_type == 'dict':
                if key == 'toyboxes':
                    self.json_toyboxes = value
                    continue
                elif key == 'config':
                    self.json_config = value
                    continue
                elif key == 'installed':
                    self.json_installed = value
                    continue

            raise SyntaxError('Incorrect format for Boxfile \'' + self.boxfile_path + '\'.\nMaybe you need to upgrade toybox?')

    def _prime_url_to_string(self):
        if self.url_to_string is None:
            self.url_to_string = {}

            if self.json_toyboxes is not None:
                for url_as_string in self.json_toyboxes.keys():
                    self.url_to_string[Url(url_as_string)] = url_as_string

    def stringForUrl(self, url):
        self._prime_url_to_string()

        return self.url_to_string.get(url)

    def addDependencyWithURLAndVersions(self, url, versions_as_string):
        if self.json_toyboxes is None:
            self.json_toyboxes = self.json_content['toyboxes'] = {}

        self.json_toyboxes[url.as_string] = versions_as_string

        self._prime_url_to_string()
        self.url_to_string[url] = url.as_string

        self.was_modified = True

    def removeDependencyWithURL(self, url):
        url_as_string = None

        if self.json_toyboxes is not None:
            url_as_string = self.stringForUrl(url)

        if url_as_string is None:
            raise SyntaxError('Couldn\'t find any dependency for URL \'' + url.as_string + '\'.')

        self.json_toyboxes.pop(url_as_string, None)

        if self.json_installed is not None:
            self.json_installed.pop(url.as_string, None)

        self.url_to_string.pop(url)

        self.was_modified = True

    def urls(self):
        self._prime_url_to_string()

        return list(self.url_to_string.keys())

    def versionsAsStringForUrl(self, url):
        self._prime_url_to_string()

        url_as_string = self.stringForUrl(url)
        if url_as_string is None:
            return None

        return self.json_toyboxes[url_as_string]

    def setLuaImport(self, lua_import_file):
        if self.json_config is None:
            self.json_config = self.json_content['config'] = {}

        self.json_config['lua_import'] = lua_import_file

        self.was_modified = True

    def setAssetsSubFolder(self, lua_import_file):
        if self.json_config is None:
            self.json_config = self.json_content['config'] = {}

        self.json_config['assets_sub_folder'] = lua_import_file

        self.was_modified = True

    def maybeInstalledVersionAsStringForUrl(self, url):
        if self.json_installed:
            return self.json_installed.get(url.as_string)

        return None

    def setInstalledVersionStringForDependency(self, dep, version_as_string):
        if self.json_installed is None:
            self.json_installed = self.json_content['installed'] = {}

        self.json_installed[dep.url.as_string] = version_as_string

        self.was_modified = True

    def maybeLuaImportFile(self):
        if self.json_config:
            return self.json_config.get('lua_import')

        return None

    def maybeAssetsSubFolder(self):
        if self.json_config:
            return self.json_config.get('assets_sub_folder')

        return None

    def saveIfModified(self):
        if self.was_modified:
            out_file = open(self.boxfile_path, 'w')
            json.dump(self.json_content, out_file, indent=4)

            out_file.close()

    @classmethod
    def maybeConvertOldBoxfile(cls, json_content):
        old_keys = {}

        for key in json_content.keys():
            value = json_content[key]

            if type(value).__name__ == 'str':
                old_keys[key] = value

        if len(old_keys) == 0:
            return False

        toyboxes = json_content.get('toyboxes')
        if toyboxes is None:
            toyboxes = json_content['toyboxes'] = {}

        for old_key in old_keys.keys():
            toyboxes[old_key] = old_keys[key]
            json_content.pop(old_key, None)

        return True
