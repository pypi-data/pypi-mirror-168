# -*- coding: UTF-8 -*-
"""
@File    :   BiliRpc -> tools.py
@IDE     :   PyCharm
@Time    :   2022/9/23 17:37
@Author  :   DMC ,
"""
import hashlib
import random
from typing import Optional
from bilibili.metadata.device.device_pb2 import Device
from bilibili.metadata.locale.locale_pb2 import Locale
from bilibili.metadata.network.network_pb2 import Network, NetworkType
from bilibili.metadata.metadata_pb2 import Metadata

def fakebuvid():
    mac_list = []
    for _ in range(1, 7):
        rand_str = "".join(random.sample("0123456789abcdef", 2))
        mac_list.append(rand_str)
    rand_mac = ":".join(mac_list)
    md5 = hashlib.md5()
    md5.update(rand_mac.encode())
    md5_mac_str = md5.hexdigest()
    md5_mac = list(md5_mac_str)
    return f"XY{md5_mac[2]}{md5_mac[12]}{md5_mac[22]}{md5_mac_str}".upper()


def make_metadata(buvid,access_token: Optional[str] = None):

    device_params = {
        "mobi_app": "android",
        "device": "phone",
        "build": 6550400,
        "channel": "bili",
        "buvid": buvid,
        "platform": "android",
    }
    metadata_params = device_params.copy()
    if access_token:
        metadata_params["access_key"] = access_token
    metadata = {
        "x-bili-device-bin": Device(**device_params).SerializeToString(),
        "x-bili-local-bin": Locale().SerializeToString(),
        "x-bili-metadata-bin": Metadata(**metadata_params).SerializeToString(),
        "x-bili-network-bin": Network(type=NetworkType.WIFI).SerializeToString(),
    }
    if access_token:
        metadata["authorization"] = f"identify_v1 {access_token}".encode()
    return tuple(metadata.items())
