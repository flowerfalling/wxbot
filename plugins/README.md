# 插件开发指南

## 示例

```python
import asyncio

import aiohttp
from wcferry import WxMsg

from plugins import register
from suswx.common import wcf, logger


@register(fromFriend=True, mode="async", check=[lambda msg: msg.content == "@一言"])
async def hitokoto(msg: WxMsg) -> None:
    """
    Hitokoto, represents the touch of words and the communication of souls
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://v1.hitokoto.cn") as resp:
                r = await asyncio.wait_for(resp.json(), timeout=5)
                wcf.send_text(info := f'{r["hitokoto"]}\n----{r["from"]}[{r["from_who"]}]', msg.sender)
    except asyncio.TimeoutError:
        wcf.send_text(info := "Sorry, hitokoto timed out", msg.sender)
    logger.info(info)
```

## 详细

```python
from typing import Callable, Optional

from wcferry import WxMsg

from suswx import Content
from suswx.Registry import func_startup_mode


#  func_startup_mode = Literal["mt", "async"]
def register(
        msgType: tuple[Content] = (Content.TEXT,),
        fromFriend: bool = False,
        fromGroup: bool = False,
        fromAdmin: bool = False,
        name: Optional[str] = None,
        mode: func_startup_mode = "mt",
        enable: bool = True,
        access: Optional[set] = None,
        check: Sequence[Callable[[WxMsg], None]] = None,
        frozen: bool = False,
        save_config: bool = True
) -> Callable[[Callable[[WxMsg], None]], None]:
    ...
```

- msgType: 接受的消息类型的元组, 默认为仅文本
- fromFriend: 是否接收来自朋友的信息
- fromGroup: 是否接收来自群聊的信息
- fromAdmin: 是否接收来自管理员的信息
- name: 功能名称, 默认为函数名, 是功能的唯一标识, 不可重复
- mode: 启动方式, "mt"为线程池运行, "async"为异步运行(函数必须为异步函数)
- enable: 是否开启功能
- access: 白名单(微信号元组, 若元组中含"ALL"则全部通过)
- check: 其他检查消息是否符合功能要求的方法序列, 方法将在主线程运行(一些简单的判断尽量写在这里, 可减少线程池资源消耗)
- frozen: 是否冻结功能, 设置为True则管理员无法更改功能状态参数
- save_config: 是否在config.yaml中创建条目来保存功能状态信息(enable和access), 若已存在条目则会加载
