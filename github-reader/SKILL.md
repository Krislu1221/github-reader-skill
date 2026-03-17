# GitHub Reader Skill v3.1

**深度解读 GitHub 项目 / Deeply Analyze GitHub Projects**

📖 自动解读 GitHub 项目，生成结构化分析报告  
📖 Automatically analyze GitHub projects and generate structured analysis reports

---

## 🚀 安装 / Installation

```bash
cd github-reader/
./install_v3_secure.sh
```

然后重启你的 Agent gateway / Then restart your Agent gateway:
```bash
# OpenClaw / 其他兼容平台 / Other compatible platforms
openclaw gateway restart
# 或 / or
<your-platform> gateway restart
```

---

## 💡 用法 / Usage

### 命令方式 / Command Mode
```
/github-read microsoft/BitNet
```

### 自然语言 / Natural Language
```
帮我解读这个仓库：https://github.com/HKUDS/nanobot
Help me analyze this repo: https://github.com/HKUDS/nanobot
```

### 简短格式 / Short Format
```
分析 HKUDS/nanobot
Analyze HKUDS/nanobot
```

---

## 📊 输出示例 / Output Example

```markdown
好的！已经抓取到相关项目的详细信息，让我来为您解读：
Great! I've captured detailed information about the project, let me analyze it for you:

# 📦 microsoft/BitNet 深度解读报告
# microsoft/BitNet In-depth Analysis Report

> **分析时间 / Analysis Time**: 2026-03-13 01:27  
> **数据来源 / Data Sources**: Zread 深度解读 + 技术社区 + 互联网信息，仅供参考  
> **Data Sources**: Zread in-depth analysis + Tech community + Internet information, for reference only

---

## 💡 一句话介绍 / One-Sentence Introduction
BitNet.cpp 是微软官方推出的 1 比特量化大语言模型推理框架...  
BitNet.cpp is Microsoft's official 1-bit quantized LLM inference framework...

## 📊 项目卡片 / Project Cards
| 指标 / Metric | 值 / Value |
|------|-----|
| ⭐ Stars | 12.5k |
| 🍴 Forks | 2.1k |
| 📝 Issues | 156 |
| 🐍 语言 / Language | Python |
| 📄 许可证 / License | MIT License |

## 🔗 快速链接 / Quick Links
| 平台 / Platform | 链接 / Link | 说明 / Description |
|------|------|------|
| **GitHub** | https://github.com/microsoft/BitNet | 源代码仓库 / Source code repository |
| **Zread** | https://zread.ai/microsoft/BitNet | 📖 深度解读（推荐）/ In-depth analysis (Recommended) |
| **GitView** | http://localhost:8080/?repo=microsoft/BitNet | 🚀 快速概览（可选）/ Quick overview (Optional) |

> **注意 / Note**: 
> - Zread 是第三方深度代码解读服务（可选）/ Zread is a third-party code analysis service (optional)
> - GitView 需要本地运行（可选）/ GitView requires local setup (optional)
> - GitHub 是必需的代码源 / GitHub is the required code source
```

---

## 🛡️ 安全特性 / Security Features (v3.0)

### P0 级别（高危修复）/ P0 Level (Critical Fixes)
- ✅ **输入验证** / **Input Validation** - 防止 URL 注入 / Prevents URL injection
- ✅ **安全 URL 拼接** / **Safe URL Joining** - 防止 SSRF / Prevents SSRF attacks
- ✅ **缓存数据验证** / **Cache Data Validation** - 防止投毒 / Prevents poisoning
- ✅ **路径安全检查** / **Path Security Check** - 防止遍历 / Prevents traversal

### P1 级别（中危修复）/ P1 Level (Medium Fixes)
- ✅ **浏览器并发限制** / **Browser Concurrency Limit**
- ✅ **API 频率限制** / **API Rate Limiting**
- ✅ **超时控制** / **Timeout Control**

---

## ⚙️ 配置 / Configuration

### 环境变量 / Environment Variables

```bash
# 缓存配置 / Cache Configuration
export GITVIEW_CACHE_DIR="/tmp/gitview_cache"  # 缓存目录 / Cache directory
export GITVIEW_CACHE_TTL="24"                   # 缓存时间（小时）/ Cache TTL (hours)
export GITVIEW_CACHE_MAX_SIZE="1"               # 最大缓存文件（MB）/ Max cache file (MB)

# 性能配置 / Performance Configuration
export GITVIEW_MAX_BROWSER="3"                  # 最大并发浏览器 / Max concurrent browsers
export GITVIEW_GITHUB_DELAY="1.0"               # API 调用间隔（秒）/ API call delay (seconds)

# 超时配置 / Timeout Configuration
export GITVIEW_BROWSER_TIMEOUT="30"             # 浏览器超时（秒）/ Browser timeout (seconds)
export GITVIEW_GITHUB_TIMEOUT="10"              # GitHub API 超时（秒）/ GitHub API timeout (seconds)
```

---

## 📈 性能指标 / Performance Metrics

| 场景 / Scenario | 耗时 / Time | 备注 / Notes |
|----------------|-------------|--------------|
| 首次分析 / First analysis | 10-15 秒 / seconds | 抓取 + 分析 / Fetch + Analyze |
| 缓存命中 / Cache hit | < 1 秒 / second | 直接返回 / Direct return |
| 缓存过期 / Cache expiry | 12-24 小时 / hours | 可配置 / Configurable |

---

## 📁 文件结构 / File Structure

```
github-reader/
├── github_reader_v3_secure.py       # v3.0 主代码 / v3.0 Secure main code
├── __init__.py                      # Skill 注册 / Skill registration
├── clawhub.json                     # ClawHub 元数据 / ClawHub metadata
├── SECURITY.md                      # 安全指南 / Security guide
├── RELEASE_NOTES.md                 # 发布说明 / Release notes
├── README_BILINGUAL.md              # 简洁中英对照 / Concise bilingual README
├── README_EN_CN.md                  # 详细中英对照 / Detailed bilingual README
├── PACKAGE.md                       # 打包说明 / Package guide
└── install_v3_secure.sh             # 安装脚本 / Installation script
```

---

## 🔧 技术栈 / Tech Stack

- **语言 / Language**: Python 3.9+
- **依赖 / Dependencies**: OpenClaw compatible platform
- **工具 / Tools**: web_fetch, browser
- **缓存 / Cache**: 文件系统缓存（JSON 格式）/ File system cache (JSON format)
- **并发 / Concurrency**: asyncio 异步编程 / asyncio async programming

---

## 📞 支持 / Support

- **GitHub Issues**: https://github.com/your-repo/github-reader-skill/issues
- **讨论区 / Discussions**: https://github.com/your-repo/github-reader-skill/discussions
- **文档 / Documentation**: See README_EN_CN.md for full documentation

---

## 📄 许可证 / License

MIT License

---

## 👨💻 作者 / Author

**Krislu + 🦐 虾软**

---

*版本 / Version: v3.1（安全加固版 / Security Hardened）*  
*最后更新 / Last Updated: 2026-03-13*
