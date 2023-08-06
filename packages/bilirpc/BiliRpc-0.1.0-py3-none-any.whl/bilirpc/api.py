# -*- coding: UTF-8 -*-
"""
@File    :   BiliRpc -> api.py
@IDE     :   PyCharm
@Time    :   2022/9/23 17:34
@Author  :   DMC ,
"""
from typing import Optional

import grpc

from bilibili.app.dynamic.v2.dynamic_pb2 import (
    DynAllReq,
    DynamicType,
    DynSpaceReq,
    DynDetailsReq,
)
from bilibili.app.dynamic.v2.dynamic_pb2_grpc import DynamicStub
from tools import fakebuvid, make_metadata


async def get_follow_dynamic(update_baseline: Optional[str], access_token: str):
    try:
        async with grpc.aio.secure_channel(
                "grpc.biliapi.net",
                grpc.ssl_channel_credentials()) as channel:
            stub = DynamicStub(channel=channel)
            if update_baseline:
                req = DynAllReq(update_baseline=update_baseline, refresh_type=1)
            else:
                req = DynAllReq(refresh_type=1)
            resp = await stub.DynAll(req, metadata=make_metadata(buvid=fakebuvid(),
                                                                 access_token=access_token))
            exclude_list = [
                DynamicType.ad,
                DynamicType.live,
                DynamicType.live_rcmd,
                DynamicType.banner,
            ]
            dynamic_list = [
                dyn for dyn in resp.dynamic_list.list if dyn.card_type not in exclude_list
            ]
            return dynamic_list
    except Exception as e:
        return


async def get_dy_detail(dynamic_id):
    try:
        async with grpc.aio.secure_channel(
                "grpc.biliapi.net",
                grpc.ssl_channel_credentials()) as channel:
            stub = DynamicStub(channel=channel)
            req = DynDetailsReq(dynamic_ids=dynamic_id, local_time=8)
            result = await stub.DynDetails(req, metadata=make_metadata(buvid=fakebuvid()))
            return result.list
    except Exception as e:
        return None


async def get_space_dynamic(uid):
    try:
        async with grpc.aio.secure_channel(
                "grpc.biliapi.net",
                grpc.ssl_channel_credentials()) as channel:
            stub = DynamicStub(channel=channel)
            req = DynSpaceReq(host_uid=uid, local_time=8)
            result = await stub.DynSpace(req, metadata=make_metadata(buvid=fakebuvid()))
            return result.list
    except Exception as e:
        return None

async def main():
    dynamic = await get_dy_detail("708588459211620393")

    pic = await Render().run(dynamic[0])
    with open("1.png","wb") as f:
        f.write(pic)


if __name__ == '__main__':
    from dynamicrendergrpc.Core.Dynamic import Render
    import asyncio
    asyncio.run(main())
