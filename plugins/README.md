# Plugin Development Guide

<p align="center">
English | <a href="README_zh.md">简体中文</a>
</p>

## Example

1. Create a python package in the plugins directory, here named **funcs**
2. Create the required module in funcs, here named **hitokoto**
3. Register the function **hitokoto** in hitokoto.py
4. Add hitokoto record in \_\_all\_\_ of plugins\\funcs\\_\_init\_\_.py
5. Add this python **package name** to the **plugins-list** entry in **config.yaml**

```python
# plugins\\funcs\\__init__.py
__all__ = ["hitokoto"]
```

```python
# plugins\\funcs\\hitokoto.py
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

```yaml
# config.yaml
plugins:
  info: {}
  list:
  - funcs
```

## Detail

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

- msgType: a tuple of Message types allowed to be processed
- fromFriend: Whether to handle messages from friends
- fromGroup: Whether to handle messages from groups
- fromAdmin: Whether to handle messages from the admin
- name: Function name (Optional, default is function name)
- mode: Function startup method (multithreaded "mt" or asynchronous "async")
- enable: Whether to enable
- access: The set of wxids of allowed message senders(Optional)
- check: Other sequence of methods to check whether the message meets the conditions
- frozen: Whether to freeze this function (cannot be modified)
- save_config: Whether to set default configuration, including access and enable, and will be written to config.yaml