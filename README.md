# Wxbot

Papersus's Wxbot is a WeChat bot with ChatGPT(only Windows)

WeChat robot framework and examples based on wcferry

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

```Python
# Update pip
python -m pip install -U pip

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `config.yaml` file and then enter the configuration in the `config.template.yaml` style

### Get Start

```Python
python demo.py

# To stop, press Ctrl+C
```

#### Users(your friends)

```Text
gpt command:
  /xxx 与gpt对话
  /gpt help 获取帮助
  /gpt start 开启gpt连续对话
  /gpt end 关闭gpt连续对话
  /gpt clear 清空当前会话
```

#### Administrator(you)

```Text
gpt command[me]
  /gpt start 开启gpt
  /gpt stop 关闭gpt
  /gpt enable username 开启用户gpt权限
  /gpt disable username 关闭用户gpt权限
  /gpt help 获取帮助
```

## Do not abuse

I **picked up** this API and it could have serious consequences if misused
