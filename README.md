# Wxbot

<p align="center">
English | <a href="README_zh.md">简体中文</a>
</p>

Papersus Wxbot is a WeChat bot with ChatGPT(only Windows)

WeChat robot framework and examples based on [wcferry](https://github.com/lich0821/WeChatFerry)

<details><summary>Disclaimer[mandatory reading]</summary>

The author of this tool makes no warranty, express or implied, as to the safety, completeness, reliability, validity, correctness, or suitability of this tool, and assumes no responsibility for any direct or indirect loss, liability, claim, demand, or action resulting from the use or misuse of this tool.

The author of this tool reserves the right to modify, update, delete or terminate this tool at any time without prior notice or obligation.

Users of the Tool shall comply with relevant laws and regulations, respect WeChat's copyright and privacy, and shall not infringe upon the legitimate rights and interests of WeChat or other third parties, or engage in any illegal or unethical behavior.

By downloading, installing, running or using the Tool, users of the Tool acknowledge that they have read and agree to this disclaimer. If you have any objection, please stop using the Tool immediately and delete all related files.

</details>

## Basic Usage

Now the bot only supports private chats, and does not support group chats for the time being

### Environment

- Python `>=3.10`
- WeChat `3.9.2.23`

### deploy

```Shell
git clone https://github.com/flowerfalling/wxbot.git
```

_Download WeChat version 3.9.3.23 
[Here](https://github.com/lich0821/WeChatFerry/releases/download/v39.0.12/WeChatSetup-3.9.2.23.exe)_

### Dependencies

```Shell
# Update pip
python -m pip install -U pip

# Install dependencies
pip install -r requirements.txt
```

### Get Start

```Shell
python SusRobot.py

# To stop, press Ctrl+C
```

_Please use the administrator to set users who allow the bot function to reply, see details below (/enable)_

The administrator(the default is wechat for bot login) sends `/enable username all` in the WeChat private message to enable all functions for the specified user.

The user sends `@menu` to get the function list and use the function

<details><summary>Feature</summary>

#### Users' command(your friends)

```Text
@菜单  # get the menu
@一言  # get a sentence
@历史上的今天  # get ten events from today in history
@微博/知乎热搜  # get the ten hot searches on Weibo/Zhihu
@星座运势 xxx  # get today's horoscope picture
```

```Text
gpt command:
/xxx  # Talk to GPT
/gpt help  # Get help
/gpt start  # Enable GPT continuous conversation
/gpt end  # Disable GPT continuous conversation
/gpt clear  # Clear current session records
```

```Text
gemini command:
%xxx  # Talk to Gemini
%gemini help  # Get help
%gemini start  # Enable Gemini continuous conversation
%gemini end  # Disable Gemini continuous conversation
%gemini clear  # Clear current session records
```

#### Administrator's command(you)

The following functions are currently available:

- menu
- gpt
- gemini
- hitokoto

Call any of them func

```Text
Administrator documentation
  /help  # Get help
  /state  # View functions' status
  /config  # Reload configuration file
  /disable|enable name1[,name2[...]] func1[,func2[...]]|all  # Enable|Disable someone's permission for some|all functions
  /start|stop func1[,func2[,func3[...]]  # Start|Stop functions
  /admin name  # Transfer administrator's identity
  /quit  # Exit robot
```

_Gimini is not enabled by default, please fill in the token in plugins-info-gemini-token in config.yaml then restart (then enbale it)_
</details>

## Do not abuse gpt

I **picked up** this gpt API, so it could have serious consequences if misused

## Plugin development

See at [Plugin Development Guide](./plugins/README.md)
