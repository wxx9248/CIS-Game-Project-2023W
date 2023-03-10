# -*- coding: utf-8 -*-
import logging
import os
import typing

import pygame.image

from core.object_model.Map import Map
from core.object_model.Sound import Sound
from core.object_model.Sprite import Sprite
from core.object_model.Text import Text


class AssetObjectFactory:
    ASSET_DIRS = ("asset/images", "asset/sounds", "asset/texts")
    ASSET_PROPS = {
        "asset/images/pickle-0.png": {"key": "asset.sprite.pickle.0"},
        "asset/images/pickle-1.png": {"key": "asset.sprite.pickle.1"},
        "asset/images/pickle-2.png": {"key": "asset.sprite.pickle.2"},
        "asset/images/senior-pickle.png": {"key": "asset.sprite.senior-pickle"},
        "asset/images/bacteria.png": {"key": "asset.sprite.bacteria"},
        "asset/images/boss.png": {"key": "asset.sprite.boss"},
        "asset/images/heart.png": {"key": "asset.sprite.heart"},
        "asset/images/pickle-projectile.png": {"key": "asset.sprite.pickle-projectile"},
        "asset/images/boss-projectile.png": {"key": "asset.sprite.boss-projectile"},
        "asset/images/level-0/background.jpg": {"key": "asset.sprite.level.0.background"},
        "asset/images/level-0/tile/soil.png": {"key": "asset.sprite.level.0.tile.soil"},
        "asset/images/level-0/tile/wall.png": {"key": "asset.sprite.level.0.tile.wall"},
        "asset/images/level-0/tile/exit.png": {"key": "asset.sprite.level.0.tile.exit"},
        "asset/images/level-0/tile/spawn.jpg": {"key": "asset.sprite.level.0.tile.spawn"},
        "asset/images/level-0-plus/background.jpg": {"key": "asset.sprite.level.0.plus.background"},
        "asset/images/level-1/background.png": {"key": "asset.sprite.level.1.background"},
        "asset/images/level-1/tower.png": {"key": "asset.sprite.level.1.tower"},
        "asset/images/level-1/tree.png": {"key": "asset.sprite.level.1.tree"},
        "asset/images/level-1/tile/grass.png": {"key": "asset.sprite.level.1.tile.grass"},
        "asset/images/level-1/tile/soil.png": {"key": "asset.sprite.level.1.tile.soil"},
        "asset/images/level-1/tile/water.png": {"key": "asset.sprite.level.1.tile.water"},
        "asset/images/menu-background.png": {"key": "asset.sprite.menu.background"},
        "asset/images/help-manual.png": {"key": "asset.sprite.help-manual"},
        "asset/texts/menu-logo.png": {"key": "asset.sprite.menu.logo"},
        "asset/texts/menu-start.png": {"key": "asset.sprite.menu.start"},
        "asset/texts/menu-help.png": {"key": "asset.sprite.menu.help"},
        "asset/texts/menu-exit.png": {"key": "asset.sprite.menu.exit"},
        "asset/texts/menu-cursor.png": {"key": "asset.sprite.menu.cursor"},
        "asset/texts/game-lost.png": {"key": "asset.sprite.game-lost"},
        "asset/texts/game-win.png": {"key": "asset.sprite.game-win"},
        "asset/texts/retry.png": {"key": "asset.sprite.retry"},
        "asset/texts/next-level.png": {"key": "asset.sprite.next-level"},
        "asset/texts/back-to-menu.png": {"key": "asset.sprite.back-to-menu"},
        "asset/texts/help-back-hint.json": {"key": "asset.text.help.back-hint"},
        "asset/maps/level-0.csv": {"key": "asset.map.level.0"},
        "asset/maps/level-1.csv": {"key": "asset.map.level.1"},
        "asset/maps/level-2.csv": {"key": "asset.map.level.2"},
        None: {"key": "asset.map.random"}
    }

    __asset_id_path_dict = {value["key"]: key for key, value in ASSET_PROPS.items()}
    __instance = None

    def __new__(cls, *args, **kwargs):
        def init(instance):
            instance.__logger = logging.getLogger(instance.__class__.__name__)

            instance.__logger.info("Scanning asset directories")
            asset_file_paths = []
            for target_dir in AssetObjectFactory.ASSET_DIRS:
                instance.__logger.debug(f"Scanning {target_dir}")
                asset_file_paths.extend([os.path.join(directory, file)
                                         for directory, _, filenames in os.walk(target_dir)
                                         for file in filenames])

            instance.__logger.debug(f"Scan result: {asset_file_paths}")

            for path in asset_file_paths:
                path not in AssetObjectFactory.ASSET_PROPS and instance.__logger.warning(
                    f"Asset {path} is not assigned with an key, thus not addressable with asset manager"
                )

        if cls.__instance is None:
            cls.__instance = super(AssetObjectFactory, cls).__new__(cls)
            init(cls.__instance)

        return cls.__instance

    def new_asset_object(self, asset_key: str, *args, **kwargs) -> typing.Any:
        self.__logger.debug(f"Creating asset object with asset key {asset_key}")
        fields = asset_key.split('.')
        namespace = fields[0]
        asset_type = fields[1]

        if namespace != "asset":
            self.__logger.warning(f"Not an asset key. Object not created")
            return

        if asset_type == "sprite":
            self.__logger.debug("Creating a sprite object")
            return Sprite(pygame.image.load(AssetObjectFactory.__asset_id_path_dict[asset_key]), *args, **kwargs)
        if asset_type == "sound":
            self.__logger.debug("Creating a sound object")
            return Sound(AssetObjectFactory.__asset_id_path_dict[asset_key], *args, **kwargs)
        if asset_type == "text":
            self.__logger.debug("Creating a text object")
            return Text(AssetObjectFactory.__asset_id_path_dict[asset_key], *args, **kwargs)
        if asset_type == "map":
            self.__logger.debug("Creating a map object")
            return Map(AssetObjectFactory.__asset_id_path_dict[asset_key], *args, **kwargs)

        self.__logger.debug(f"Unknown asset type {asset_type}. Object not created")
        return
