# GitHub Reader Skill v3.1

**深度解读 GitHub 项目 / Deeply Analyze GitHub Projects**

📖 自动解读 GitHub 项目，生成结构化分析报告  
📖 Automatically analyze GitHub projects and generate structured analysis reports

---

## 设计理念

GitHub Reader 的核心思路是**组合三个来源的数据**生成一份完整的项目解读报告：

1. **GitHub REST API** — 实时元数据（Stars、Forks、Issues、语言、许可证）
2. **Zread** — 第三方深度代码解读（架构分析、性能基准、功能拆解）
3. **结构化模板** — 统一的 Markdown 报告格式，确保每次输出一致

这三个来源互补：GitHub API 给"事实"，Zread 给"深度分析"，模板给"一致性"。

### 核心设计原则

- **输入安全优先** — 所有 repo/owner 名经过严格白名单校验，防止 URL 注入和路径遍历
- **无外部依赖** — GitHub API 使用标准库 `urllib`，不需要第三方 HTTP 包
- **工具注入模式** — `web_fetch` 通过构造函数注入而非 import，解耦运行环境
- **缓存与防抖** — 24 小时文件缓存 + API 速率限制，防止重复请求

---

## 🚀 安装 / Installation

```bash
cd github-reader/
./install_v3_secure.sh
```

然后重启你的 Agent gateway：
```bash
openclaw gateway restart
```

---

## 💡 用法 / Usage

### 命令方式
```
/github-read microsoft/BitNet
```

### 自然语言
```
帮我解读这个仓库：https://github.com/HKUDS/nanobot
```

### 简短格式
```
分析 HKUDS/nanobot
```

---

## 📊 输出示例

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

### P0 级别（高危修复）
- ✅ **输入验证** — 只允许 `[a-zA-Z0-9._-]`，防 URL 注入
- ✅ **安全 URL 拼接** — `urllib.parse.quote` 编码路径组件，防 SSRF
- ✅ **缓存数据验证** — JSON 结构校验 + 文件大小限制，防投毒
- ✅ **路径安全检查** — 绝对路径规范化 + 目录边界检查，防遍历

### P1 级别（中危修复）
- ✅ **API 频率限制** — GitHub API 调用间隔 ≥1 秒
- ✅ **超时控制** — API 10 秒超时，防止无限挂起

---

## ⚙️ 配置

### 环境变量

```bash
# 缓存配置
export GITVIEW_CACHE_DIR="/tmp/gitview_cache"  # 缓存目录
export GITVIEW_CACHE_TTL="24"                   # 缓存时间（小时）
export GITVIEW_CACHE_MAX_SIZE="1"               # 最大缓存文件（MB）

# 速率限制
export GITVIEW_GITHUB_DELAY="1.0"               # API 调用间隔（秒）
export GITVIEW_GITHUB_TIMEOUT="10"              # API 超时（秒）
```

---

## 📁 文件结构

```
github-reader/
├── github_reader_v3_secure.py       # v3.1 主代码
├── __init__.py                      # Skill 注册
├── clawhub.json                     # ClawHub 元数据
├── SKILL.md                         # 本文档
├── README.md                        # GitHub README
├── SECURITY.md                      # 安全指南
├── RELEASE_NOTES.md                 # 发布说明
├── PACKAGE.md                       # 打包说明
└── install_v3_secure.sh             # 安装脚本
```

---

## 🔧 技术栈

- **语言**: Python 3.9+
- **HTTP 客户端**: `urllib`（标准库，零额外依赖）
- **缓存**: 文件系统（JSON 格式）
- **安全哈希**: MD5（缓存去重，非安全用途）

---

## 👨‍💻 作者

Kris Lu <krislu666@foxmail.com>

## 📄 许可证

MIT License

---

*版本: v3.1.4 · 最后更新: 2026-05-23*
