# Wxbot

<p align="center">
简体中文 | <a href="README.md">English</a>
</p>

Papersus Wxbot 是一个带有 ChatGPT 的微信机器人（仅限 Windows）

是一个基于[wcferry](https://github.com/lich0821/WeChatFerry)的微信机器人框架及示例

<details><summary>免责声明【必读】</summary>

本工具仅供学习和技术研究使用，不得用于任何商业或非法行为，否则后果自负。

本工具的作者不对本工具的安全性、完整性、可靠性、有效性、正确性或适用性做任何明示或暗示的保证，也不对本工具的使用或滥用造成的任何直接或间接的损失、责任、索赔、要求或诉讼承担任何责任。

本工具的作者保留随时修改、更新、删除或终止本工具的权利，无需事先通知或承担任何义务。

本工具的使用者应遵守相关法律法规，尊重微信的版权和隐私，不得侵犯微信或其他第三方的合法权益，不得从事任何违法或不道德的行为。

本工具的使用者在下载、安装、运行或使用本工具时，即表示已阅读并同意本免责声明。如有异议，请立即停止使用本工具，并删除所有相关文件。

</details>

## 基本用法

目前机器人仅支持私聊，暂时不支持群聊

### 环境

- Python `>=3.9`
- WeChat `3.9.2.23`

### 部署

```Shell
git clone https://github.com/flowerfalling/wxbot.git
```

_[在这里](https://github.com/lich0821/WeChatFerry/releases/download/v39.0.12/WeChatSetup-3.9.2.23.exe)下载微信版本3.9.3.23_

### 依赖

```Shell
# 更新 pip
python -m pip install -U pip

# 安装 依赖
pip install -r requirements.txt
```

### 开始使用

```Shell
python SusRobot.py

# 要停止，请按 Ctrl+C
```

<details><summary>详情</summary>

#### 用户命令（你的朋友）

```Text
@菜单  # 获取菜单
```

```Text
@一言  # 得到一个句子
```

```Text
gpt command:
/xxx  # 与 GPT 交谈
/gpt help  # 得到帮助
/gpt start  # 启用 GPT 连续对话
/gpt end  # 禁用 GPT 连续对话
/gpt clear  # 清除当前会话记录
```

```Text
gemini command:
%xxx  # 与 Gemini 交谈
%gemini help  # 得到帮助
%gemini start  # 启用 Gemini 持续对话
%gemini end  # 禁用 Gemini 连续对话
%gemini clear  # 清除当前会话记录
```

#### 管理员命令（您）

目前可以使用以下功能：

- menu
- gpt
- gemini
- hitokoto

称其中任意一个 func

```Text
Administrator documentation
  /help  # 得到帮助
  /state  # 查看功能的状态
  /config  # 重新载入配置文件
  /disable|enable name1[,name2[...]] func1[,func2[...]]|all  # 启用|禁用某人对部分|所有功能的权限
  /start|stop func1[,func2[,func3[...]]  # 开始|停止功能
  /admin name  # 转移管理员身份
  /quit  # 退出机器人
```

_Gimini默认不启用，请填写config.yaml中plugins-info-gemini-token并重启（然后enbale）_
</details>
