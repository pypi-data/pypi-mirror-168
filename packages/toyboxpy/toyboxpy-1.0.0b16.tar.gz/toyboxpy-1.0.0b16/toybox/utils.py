# SPDX-FileCopyrightText: 2022-present Paths.py Contributors
#
# SPDX-License-Identifier: MIT

import os
import shutil

from pathlib import Path


class Utils:
    """Utility methods used by toyboxpy."""

    @classmethod
    def lookInFolderFor(cls, folder, wildcard):
        # -- We use this here instead of just simply os.path.exists()
        # -- because we want the test to be case-sensitive on all platforms,
        # -- so we list what the match are and let glob give us the paths.
        paths_found = []
        looking_in = Path(folder)

        for p in looking_in.glob(wildcard):
            as_string = str(p)
            if len(as_string) > 4:
                as_string = as_string[len(folder) + 1:-4]
                paths_found.append(as_string)

        return paths_found

    @classmethod
    def backup(cls, from_folder, to_folder):
        if os.path.exists(from_folder):
            shutil.move(from_folder, to_folder)

    @classmethod
    def restore(cls, from_folder, to_folder):
        if os.path.exists(to_folder):
            shutil.rmtree(to_folder)

        if os.path.exists(from_folder):
            shutil.move(from_folder, to_folder)

    @classmethod
    def delete(cls, folder):
        if os.path.exists(folder):
            shutil.rmtree(folder)
