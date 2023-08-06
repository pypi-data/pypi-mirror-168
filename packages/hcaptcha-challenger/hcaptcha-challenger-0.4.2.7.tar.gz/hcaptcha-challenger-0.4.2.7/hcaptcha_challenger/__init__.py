# -*- coding: utf-8 -*-
# Time       : 2022/2/15 17:43
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import os
import shutil
import time
import typing

from ._scaffold import init_log, Config, get_challenge_ctx
from ._solutions.kernel import PluggableObjects
from ._solutions.yolo import YOLO, Prefix
from .core import HolyChallenger

__all__ = ["HolyChallenger", "new_challenger", "get_challenge_ctx"]
__version__ = "0.4.2.7"

logger = init_log(
    error=os.path.join("datas", "logs", "error.log"),
    runtime=os.path.join("datas", "logs", "runtime.log"),
)


def install(
    onnx_prefix: typing.Optional[str] = Prefix.YOLOv6n, upgrade: typing.Optional[bool] = False
):
    """

    :param onnx_prefix:
    :param upgrade:
    :return:
    """
    os.makedirs(Config.DIR_ASSETS, exist_ok=True)

    if not hasattr(Prefix, onnx_prefix):
        onnx_prefix = Prefix.YOLOv6n

    if upgrade is True:
        logger.debug(f"Reloading the local cache of Assets {Config.DIR_ASSETS}")
        shutil.rmtree(Config.DIR_ASSETS, ignore_errors=True)

    if (
        upgrade is True
        or not os.path.exists(Config.PATH_OBJECTS)
        or not os.path.getsize(Config.PATH_OBJECTS)
        or time.time() - os.path.getmtime(Config.PATH_OBJECTS) > 3600
    ):
        PluggableObjects(path_objects=Config.PATH_OBJECTS).sync()
    YOLO(dir_model=Config.DIR_MODEL, onnx_prefix=onnx_prefix).pull_model().offload()


def new_challenger(
    dir_workspace: str = "_challenge",
    onnx_prefix: typing.Optional[str] = Prefix.YOLOv6n,
    lang: typing.Optional[str] = "en",
    screenshot: typing.Optional[bool] = False,
    debug: typing.Optional[bool] = False,
) -> HolyChallenger:
    """

    :param dir_workspace:
    :param onnx_prefix:
    :param lang:
    :param screenshot:
    :param debug:
    :return:
    """
    if not isinstance(dir_workspace, str) or not os.path.isdir(dir_workspace):
        dir_workspace = os.path.join("datas", "temp_cache", "_challenge")
        os.makedirs(dir_workspace, exist_ok=True)
    if not hasattr(Prefix, onnx_prefix):
        onnx_prefix = Prefix.YOLOv6n

    return HolyChallenger(
        dir_workspace=dir_workspace,
        dir_model=Config.DIR_MODEL,
        path_objects_yaml=Config.PATH_OBJECTS,
        lang=lang,
        onnx_prefix=onnx_prefix,
        screenshot=screenshot,
        debug=debug,
    )
