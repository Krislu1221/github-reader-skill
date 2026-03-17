# 📦 GitHub Reader Skill v3.1

**深度解读 GitHub 项目 / Deeply Analyze GitHub Projects**

---

## 🎯 简介 / Introduction

**中文**: GitHub Reader Skill 是一个强大的 AI 工具，只需输入 GitHub 仓库链接，即可自动生成深度分析报告，包括技术架构、性能基准、应用场景等。

**English**: GitHub Reader Skill is a powerful AI tool that automatically generates in-depth analysis reports including technical architecture, performance benchmarks, and application scenarios by simply inputting a GitHub repository link.

---

## ⚡ 快速开始 / Quick Start

### 安装 / Install

```bash
# 使用 ClawHub / Using ClawHub
clawhub install github-reader

# 或手动安装 / Or manual installation
cd github-reader/
./install_v3_secure.sh
```

### 使用 / Usage

```bash
# 命令模式 / Command mode
/github-read microsoft/BitNet

# 自然语言 / Natural language
帮我解读这个仓库 / Help me analyze this repo
```

---

## 🛡️ 安全特性 / Security Features

- ✅ **输入验证** / **Input Validation** - 防止 URL 注入 / Prevents URL injection
- ✅ **URL 编码** / **URL Encoding** - 防止 SSRF 攻击 / Prevents SSRF attacks
- ✅ **缓存验证** / **Cache Validation** - 防止数据投毒 / Prevents data poisoning
- ✅ **并发控制** / **Concurrency Control** - 资源保护 / Resource protection
- ✅ **超时管理** / **Timeout Management** - 防止挂起 / Prevents hanging

---

## 📊 输出内容 / Output

分析报告包含 / Analysis report includes:

1. 💡 **一句话介绍** / **One-sentence introduction**
2. 📊 **项目卡片** / **Project cards** (Stars, Forks, Issues)
3. 🏗️ **技术架构** / **Technical architecture**
4. 📈 **性能基准** / **Performance benchmarks**
5. 🆚 **竞品对比** / **Competitor comparison**
6. 🚀 **快速开始** / **Quick start guide**
7. 📚 **学习路径** / **Learning path**

---

## ⚙️ 配置 / Configuration

```bash
# 缓存配置 / Cache settings
export GITVIEW_CACHE_TTL="24"           # 缓存时间（小时）/ Cache TTL (hours)
export GITVIEW_MAX_BROWSER="3"          # 最大并发 / Max concurrency
export GITVIEW_GITHUB_DELAY="1.0"       # API 间隔 / API delay (seconds)
```

---

## 📈 性能 / Performance

| 场景 / Scenario | 耗时 / Time |
|----------------|-------------|
| 首次分析 / First analysis | 10-15 秒 / seconds |
| 缓存命中 / Cache hit | < 1 秒 / second |

---

## 📁 文件结构 / File Structure

```
github-reader/
├── github_reader_v3_secure.py       # v3.1 主代码 / v3.1 Secure main code
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

## 🔗 相关链接 / Links

- **GitHub**: https://github.com/your-repo/github-reader-skill
- **ClawHub**: `clawhub install github-reader`
- **文档 / Docs**: See README_EN_CN.md for full documentation

---

## 📄 许可证 / License

MIT License

---

## 👨‍💻 作者 / Author

**Krislu + 🦐 虾软**

---

*版本 / Version: v3.1 (安全加固版 / Security Hardened)*  
*更新 / Updated: 2026-03-13*
