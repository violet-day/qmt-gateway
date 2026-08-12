# QMT Gateway

Windows 上的 QMT/xtquant 接入项目。

## 固定版本

- Python `3.11.13` x64
- xtquant `250807.1.2`
- 依赖管理：uv

`xtquant` 包含 Windows x64 原生扩展，因此程序必须在 Windows 上运行。

## 安装

```powershell
git clone https://github.com/violet-day/qmt-gateway.git C:\QMTGateway
Set-Location C:\QMTGateway
uv sync --frozen
```

## QMT 连通测试

先启动并登录 QMT，确认交易服务正常运行。测试脚本只查询资产，不会提交订单。

```powershell
$env:QMT_ACCOUNT_ID = "你的资金账号"
$env:QMT_USERDATA_PATH = "C:\gjzqqmt\userdata_mini"
uv run --frozen python .\test_qmt_connection.py
```

登录密码只在 QMT 客户端中输入，不写入代码、环境文件或 Git。
