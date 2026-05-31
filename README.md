# Wxbot

<p align="center">
English | <a href="README_zh.md">简体中文</a>
</p>

Papersus Wxbot is a Windows-only WeChat bot with ChatGPT support.

Built on [wcferry](https://github.com/lich0821/WeChatFerry), this repo provides a WeChat bot framework and examples.

<details><summary>Disclaimer[mandatory reading]</summary>

The author of this tool makes no warranty, express or implied, as to the safety, completeness, reliability, validity, correctness, or suitability of this tool, and assumes no responsibility for any direct or indirect loss, liability, claim, demand, or action resulting from the use or misuse of this tool.

The author of this tool reserves the right to modify, update, delete or terminate this tool at any time without prior notice or obligation.

Users of the Tool shall comply with relevant laws and regulations, respect WeChat's copyright and privacy, and shall not infringe upon the legitimate rights and interests of WeChat or other third parties, or engage in any illegal or unethical behavior.

By downloading, installing, running or using the Tool, users of the Tool acknowledge that they have read and agree to this disclaimer. If you have any objection, please stop using the Tool immediately and delete all related files.

</details>

## Basic Usage

- Private chats only; group chats are not supported yet.

### Environment

- Windows
- Python `>=3.10`
- WeChat `3.9.2.23`

### Install

```Shell
git clone https://github.com/flowerfalling/wxbot.git
cd wxbot
```

_Download WeChat version 3.9.2.23
[here](https://github.com/lich0821/WeChatFerry/releases/download/v39.0.12/WeChatSetup-3.9.2.23.exe)._

### Dependencies

```Shell
# Update pip
python -m pip install -U pip

# Install dependencies
pip install -r requirements.txt
```

### Getting Started

```Shell
python SusRobot.py

# To stop, press Ctrl+C
```

_Use the administrator account to enable permissions for users (see /enable below)._

- The administrator (default: the WeChat account used to log in) sends `/enable username all` in a private chat to enable all functions for the specified user.
- Users send `@menu` to view available commands.

<details><summary>Features</summary>

#### User commands (friends)

```Text
@菜单  # get the menu
@一言  # get a sentence
@历史上的今天  # get ten events from today in history
@微博/知乎热搜  # get the ten hot searches on Weibo/Zhihu
@星座运势 xxx  # get today's horoscope picture
```

```Text
GPT commands:
/xxx  # Talk to GPT
/gpt help  # Get help
/gpt start  # Enable GPT continuous conversation
/gpt end  # Disable GPT continuous conversation
/gpt clear  # Clear current session records
```

```Text
Gemini commands:
%xxx  # Talk to Gemini
%gemini help  # Get help
%gemini start  # Enable Gemini continuous conversation
%gemini end  # Disable Gemini continuous conversation
%gemini clear  # Clear current session records
```

#### Administrator commands (you)

The following functions are currently available:

- menu
- gpt
- gemini
- hitokoto
- history
- hot_search
- constellation

Use any of the names above as the `func` parameter.

```Text
Administrator commands
  /help  # Get help
  /state  # View functions' status
  /config  # Reload configuration file
  /disable|enable name1[,name2[...]] func1[,func2[...]]|all  # Enable|Disable someone's permission for some|all functions
  /start|stop func1[,func2[,func3[...]]  # Start|Stop functions
  /admin name  # Transfer administrator's identity
  /quit  # Exit robot
```

_Gemini is disabled by default. Add your token to `plugins-info-gemini-token` in config.yaml, restart, then enable it._
</details>

## Do not abuse GPT

The GPT API key used in the demo is shared, so misuse can cause service interruptions.

## Plugin development

See at [Plugin Development Guide](./plugins/README.md)
