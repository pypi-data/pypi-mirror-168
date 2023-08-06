# SPDX-FileCopyrightText: 2022-present Paths.py Contributors
#
# SPDX-License-Identifier: MIT

import os


class Paths:
    """Various paths used by toyboxpy."""

    @classmethod
    def boxfileFolder(cls):
        return os.getcwd()

    @classmethod
    def toyboxesFolder(cls):
        return os.path.join(Paths.boxfileFolder(), 'toyboxes')

    @classmethod
    def toyboxFolderFor(cls, dep):
        return os.path.join(Paths.toyboxesFolder(), dep.subFolder())

    @classmethod
    def toyboxesBackupFolder(cls):
        return Paths.toyboxesFolder() + '.backup'

    @classmethod
    def toyboxBackupFolderFor(cls, dep):
        return os.path.join(Paths.toyboxesBackupFolder(), dep.subFolder())

    @classmethod
    def assetsFolder(cls):
        return os.path.join(Paths.boxfileFolder(), 'source', 'toybox_assets')

    @classmethod
    def assetsSubFolderFor(cls, dep):
        maybe_config_asset_folder = dep.boxfile().maybeAssetsSubFolder()
        if maybe_config_asset_folder is not None:
            return maybe_config_asset_folder
        else:
            return dep.subFolder()

    @classmethod
    def assetsFolderFor(cls, dep):
        return os.path.join(Paths.assetsFolder(), Paths.assetsSubFolderFor(dep))

    @classmethod
    def toyboxAssetsFolderFor(cls, dep):
        return os.path.join(Paths.toyboxFolderFor(dep), 'assets')

    @classmethod
    def assetsBackupFolder(cls):
        return os.path.join(Paths.toyboxesFolder(), 'assets')

    @classmethod
    def assetsBackupFolderFor(cls, dep):
        return os.path.join(Paths.toyboxesFolder(), 'assets', Paths.assetsFolderFor(dep))

    @classmethod
    def preCommitFilePath(cls):
        return os.path.join('.git', 'hooks', 'pre-commit')

    @classmethod
    def preCommitFileBackupPath(cls):
        return Paths.preCommitFilePath() + '.toyboxes_backup'

    @classmethod
    def preCommitFileNoBackupPath(cls):
        return Paths.preCommitFilePath() + '.toyboxes_no_backup'
