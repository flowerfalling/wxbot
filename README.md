# Wxbot

Papersus's Wxbot is a WeChat bot with ChatGPT(only Windows)

WeChat robot framework and examples based on wcferry

<details><summary>Disclaimer[mandatory reading]</summary>

The author of this tool makes no warranty, express or implied, as to the safety, completeness, reliability, validity, correctness, or suitability of this tool, and assumes no responsibility for any direct or indirect loss, liability, claim, demand, or action resulting from the use or misuse of this tool.

The author of this tool reserves the right to modify, update, delete or terminate this tool at any time without prior notice or obligation.

Users of the Tool shall comply with relevant laws and regulations, respect WeChat's copyright and privacy, and shall not infringe upon the legitimate rights and interests of WeChat or other third parties, or engage in any illegal or unethical behavior.

By downloading, installing, running or using the Tool, users of the Tool acknowledge that they have read and agree to this disclaimer. If you have any objection, please stop using the Tool immediately and delete all related files.

</details>

## Basic Usage

Now the bot only supports private chats, and does not support group chats for the time being

### Environment

- Python `>=3.9`
- WeChat `3.9.2.23`

### Install

```Shell
git clone https://github.com/flowerfalling/wxbot.git
```

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

<details><summary>Feature</summary>

#### Users' command(your friends)

```Text
@菜单  # get the menu
```

```Text
@一言  # get a sentence
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
  /disable|enable name1[,name2[...]] func1[,func2[...]]  # Enable | Disable someone's permission for some functions
  /start|stop func1[,func2[,func3[...]]  # Start | Stop functions
  /admin name  # Transfer administrator's identity
  /quit  # Exit robot
```

_Gimini is not enabled by default, please fill in the token in plugins-info-gemini-token in config.yaml and restart (then enbale it)_
</details>

## Do not abuse gpt

I **picked up** this gpt API, so it could have serious consequences if misused
