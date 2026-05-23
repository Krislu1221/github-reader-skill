# GitHub Reader Skill v3.1.4 - 深度解读 GitHub 项目

[![Version](https://img.shields.io/badge/version-3.1.4-blue.svg)](https://github.com/Krislu1221/github-reader-skill)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)

> 自动解读 GitHub 项目，组合 GitHub API + Zread 深度解读，生成结构化 Markdown 报告

---

## 设计理念

GitHub Reader 的核心思路是**组合三个来源的数据**生成一份完整的项目解读报告：

1. **GitHub REST API** — 实时元数据（Stars、Forks、Issues、语言、许可证）
2. **Zread** — 第三方深度代码解读（架构分析、性能基准、功能拆解）
3. **结构化模板** — 统一的 Markdown 报告格式，确保每次输出一致

### 核心设计原则

- **输入安全优先** — 所有 repo/owner 名经过严格白名单校验
- **无外部依赖** — GitHub API 使用标准库 `urllib`，不需要第三方 HTTP 包
- **工具注入模式** — `web_fetch` 通过构造函数注入而非 import
- **缓存与防抖** — 24 小时文件缓存 + API 速率限制

---

## 快速开始

### 命令方式
```
/github-read microsoft/BitNet
```

### 自然语言
```
帮我解读这个仓库：https://github.com/HKUDS/nanobot
```

### 程序调用
```python
from github_reader_v3_secure import SecureGitHubReaderV3

reader = SecureGitHubReaderV3(web_fetch_fn=web_fetch)
result = reader.analyze("microsoft", "BitNet")
print(result['full_report'])
```

---

## 输出示例

```markdown
# 📦 microsoft/BitNet 深度解读报告

> **分析时间**: 2026-05-23 23:04
> **数据来源**: GitHub API + Zread 深度解读 + 互联网信息

## 💡 一句话介绍
Official inference framework for 1-bit LLMs

## 📊 项目卡片
| 指标 | 值 |
|------|-----|
| ⭐ Stars | 39.1k |
| 🍴 Forks | 3.6k |
| 📝 Issues | 317 |
| 🐍 语言 | Python |
| 📄 许可证 | MIT |
```

---

## 🛡️ 安全特性

### P0 高危修复
- ✅ 输入验证 — 白名单正则，防 URL 注入
- ✅ 安全 URL 拼接 — `urllib.parse.quote`，防 SSRF
- ✅ 缓存数据验证 — JSON 结构校验 + 文件大小限制，防投毒
- ✅ 路径安全检查 — 绝对路径 + 目录边界，防遍历

### P1 中危修复
- ✅ API 频率限制 — ≥1秒间隔
- ✅ 超时控制 — 10秒 API 超时

---

## ⚙️ 配置

```bash
export GITVIEW_CACHE_DIR="/tmp/gitview_cache"  # 缓存目录
export GITVIEW_CACHE_TTL="24"                   # 缓存时间（小时）
export GITVIEW_GITHUB_DELAY="1.0"               # API 调用间隔（秒）
export GITVIEW_GITHUB_TIMEOUT="10"              # API 超时（秒）
```

---

## v3.1.4 vs v3.1

| 维度 | v3.1 | v3.1.4 |
|------|------|--------|
| **GitHub API** | `from openclaw.tools import web_fetch` ❌ (虚构 API) | `urllib` 标准库 ✅ |
| **Zread 抓取** | `from openclaw.tools import browser` ❌ | `web_fetch_fn` 注入 ✅ |
| **asyncio 依赖** | 全链路 async | **纯同步**，Agent 直接调用 |
| **时区处理** | `datetime.now(None)` crash | 统一 `timezone.utc` ✅ |
| **缓存键** | SHA256（无意义） | MD5（去重用途，正确） |
| **版本号** | v3.0/v3.1 混用 | 统一 v3.1.4 |
| **署名** | `🦐 虾软` | `Kris Lu` |

---

## 👤 作者

Kris Lu <krislu666@foxmail.com>

## 📄 许可

MIT License

---

*v3.1.4 · 2026-05-23*
