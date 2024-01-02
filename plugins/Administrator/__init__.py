# -*- coding: utf-8 -*-
# @Time    : 2023/12/25 22:58
# @Author  : 之落花--falling_flowers
# @File    : __init__.py.py
# @Software: PyCharm
from schema import Schema

from Configuration import config
from suswx.common import wcf, logger, botadmin

__all__ = ["Administrator"]

admin_schma = Schema({"name": object, "wxid": object})


def init_admin_config():
    me = wcf.get_user_info()
    config.config["administrator"] = {"name": me["name"], "wxid": me["wxid"]}


if not config["administrator"]:
    init_admin_config()
elif not admin_schma.is_valid(config["administrator"]):
    init_admin_config()
else:
    admin_name = str(config["administrator"]["name"])
    if admin_name is None:
        init_admin_config()
    else:
        admin = list(filter(lambda x: x["name"] == admin_name, wcf.get_friends()))
        match len(admin):
            case 0:
                logger.warning(f"Unable to find admin named {admin_name}")
                init_admin_config()
            case 1:
                config["administrator"]["name"] = admin[0]["name"]
                botadmin.wxid = config["administrator"]["wxid"] = admin[0]["wxid"]
            case _:
                logger.warning(f"You have more than one friend named {admin_name}")
                init_admin_config()

config.save_config()
admin = config["administrator"]
botadmin.wxid = admin["wxid"]
logger.info(f"Loaded admin, name: {admin['name']}, wxid: {admin['wxid']}")
