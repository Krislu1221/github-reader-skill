# GitHub Reader Skill

**GitHub Reader Skill** - 深度解读 GitHub 项目，生成结构化分析报告

**Deeply analyze GitHub projects and generate structured analysis reports**

---

## 🎯 功能特性 / Features

### 核心功能 / Core Features

- 📊 **自动分析** - 输入 GitHub URL 自动生成深度报告  
  **Auto Analysis** - Input GitHub URL to automatically generate in-depth reports

- 📖 **多维度解读** - 技术架构、性能基准、应用场景  
  **Multi-dimensional Analysis** - Technical architecture, performance benchmarks, application scenarios

- 🔗 **链接整合** - GitHub + Zread + GitView 一站式访问  
  **Link Integration** - GitHub + Zread + GitView one-stop access

- ⚡ **智能缓存** - 24 小时缓存，重复查询 < 1 秒返回  
  **Smart Caching** - 24-hour cache, repeated queries return in < 1 second

---

## 🚀 快速开始 / Quick Start

### 安装 / Installation

```bash
# 方式 1：使用 ClawHub / Method 1: Using ClawHub
clawhub install github-reader

# 方式 2：手动安装 / Method 2: Manual Installation
cd github-reader/
./install_v3_secure.sh
```

### 使用 / Usage

```bash
# 命令方式 / Command Mode
/github-read microsoft/BitNet

# 自然语言 / Natural Language
帮我解读这个仓库：https://github.com/HKUDS/nanobot
Help me analyze this repo: https://github.com/HKUDS/nanobot

# 简短格式 / Short Format
分析 HKUDS/nanobot
Analyze HKUDS/nanobot
```

---

## 🛡️ 安全特性 / Security Features

### v3.0 安全加固 / v3.0 Security Hardening

**P0 级别（高危修复） / P0 Level (Critical Fixes)**:
- ✅ 输入验证（防止 URL 注入）  
  **Input Validation** (Prevents URL injection)
- ✅ 安全 URL 拼接（防止 SSRF）  
  **Safe URL Joining** (Prevents SSRF)
- ✅ 缓存数据验证（防止投毒）  
  **Cache Data Validation** (Prevents poisoning)
- ✅ 路径安全检查（防止遍历）  
  **Path Security Check** (Prevents traversal)

**P1 级别（中危修复） / P1 Level (Medium Fixes)**:
- ✅ 浏览器并发限制  
  **Browser Concurrency Limit**
- ✅ API 频率限制  
  **API Rate Limiting**
- ✅ 超时控制  
  **Timeout Control**

---

## 📊 输出示例 / Output Example

```markdown
好的！已经抓取到相关项目的详细信息，让我来为您解读：
Great! I've captured detailed information about the project, let me analyze it for you:

# 📦 microsoft/BitNet 深度解读报告
# microsoft/BitNet In-depth Analysis Report

> **分析时间**: 2026-03-13 01:27  
> **Analysis Time**: 2026-03-13 01:27
> **数据来源**: Zread 深度解读 + 技术社区 + 互联网信息，仅供参考  
> **Data Sources**: Zread in-depth analysis + Tech community + Internet information, for reference only

---

## 💡 一句话介绍 / One-Sentence Introduction
BitNet.cpp 是微软官方推出的 1 比特量化大语言模型推理框架...  
BitNet.cpp is Microsoft's official 1-bit quantized LLM inference framework...
```

---

## ⚙️ 配置 / Configuration

### 环境变量 / Environment Variables

```bash
# 缓存配置 / Cache Configuration
export GITVIEW_CACHE_DIR="/tmp/gitview_cache"  # 缓存目录 / Cache directory
export GITVIEW_CACHE_TTL="24"                   # 缓存时间（小时）/ Cache TTL (hours)

# 性能配置 / Performance Configuration
export GITVIEW_MAX_BROWSER="3"                  # 最大并发浏览器 / Max concurrent browsers
export GITVIEW_GITHUB_DELAY="1.0"               # API 调用间隔（秒）/ API call delay (seconds)

# 超时配置 / Timeout Configuration
export GITVIEW_BROWSER_TIMEOUT="30"             # 浏览器超时（秒）/ Browser timeout (seconds)
export GITVIEW_GITHUB_TIMEOUT="10"              # GitHub API 超时（秒）/ GitHub API timeout (seconds)
```

---

## 📁 文件结构 / File Structure

```
github-reader/
├── github_reader_v3_secure.py       # v3.0 安全加固版主代码 / v3.0 Secure main code
├── __init__.py                      # Skill 注册 / Skill registration
├── clawhub.json                     # ClawHub 元数据 / ClawHub metadata
├── SECURITY.md                      # 安全配置指南 / Security guide
├── RELEASE_NOTES.md                 # 发布说明 / Release notes
├── README.md                        # 使用指南 / User guide
├── PACKAGE.md                       # 发布包说明 / Package guide
└── install_v3_secure.sh             # 安装脚本 / Installation script
```

---

## 🔧 技术栈 / Tech Stack

- **语言 / Language**: Python 3.9+
- **依赖 / Dependencies**: OpenClaw compatible platform
- **工具 / Tools**: web_fetch, browser
- **缓存 / Cache**: 文件系统缓存（JSON 格式） / File system cache (JSON format)
- **并发 / Concurrency**: asyncio 异步编程 / asyncio async programming

---

## 📈 性能指标 / Performance Metrics

| 场景 / Scenario | 耗时 / Time | 备注 / Notes |
|----------------|-------------|--------------|
| 首次分析 / First analysis | 10-15 秒 / seconds | 抓取 + 分析 / Fetch + Analyze |
| 缓存命中 / Cache hit | < 1 秒 / second | 直接返回 / Direct return |
| 缓存过期 / Cache expiry | 12-24 小时 / hours | 可配置 / Configurable |

---

## 🐛 问题反馈 / Issues

- **GitHub Issues**: https://github.com/your-repo/github-reader-skill/issues
- **讨论区 / Discussions**: https://github.com/your-repo/github-reader-skill/discussions
- **文档 / Documentation**: https://github.com/your-repo/github-reader-skill/wiki

---

## 📄 许可证 / License

MIT License

---

## 👨‍💻 作者 / Author

**Krislu + 🦐 虾软**

---

*版本 / Version: v3.1（安全加固版 / Security Hardened）*  
*最后更新 / Last Updated: 2026-03-13*
