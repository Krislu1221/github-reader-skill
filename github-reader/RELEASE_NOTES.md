# GitHub Reader Skill - ClawHub 发布说明

## 📦 发布信息

- **Skill 名称**: github-reader
- **版本**: v3.1.0（国际化安全加固版）
- **作者**: 虾软 🦐
- **描述**: 深度解读 GitHub 项目，生成结构化分析报告
- **分类**: 开发工具 / AI 助手
- **标签**: github, analysis, ai, report, zread

---

## 🎯 功能特性

### 核心功能
- 📊 **自动分析** - 输入 GitHub URL 自动生成深度报告
- 📖 **多维度解读** - 技术架构、性能基准、应用场景
- 🔗 **链接整合** - GitHub + Zread + GitView 一站式访问
- ⚡ **智能缓存** - 24 小时缓存，重复查询 < 1 秒返回

### 输出内容
- 💡 一句话介绍
- 📊 实时项目卡片（Stars/Forks/Issues）
- 🎯 核心价值主张
- 🏗️ 技术架构解析
- 📈 性能基准测试
- 🆚 竞品对比分析
- 🚀 快速上手指南
- 📚 学习路径推荐
- 🌍 社区反馈整理

---

## 🛡️ 安全特性（v3.0 新增）

### P0 级别（高危修复）
- ✅ **输入验证** - 严格的仓库名称验证（防止 URL 注入）
- ✅ **安全 URL 拼接** - 使用 `urllib.parse.quote()` 编码（防止 SSRF）
- ✅ **缓存数据验证** - 验证数据结构和大小（防止投毒）
- ✅ **路径安全检查** - 规范化文件路径（防止遍历）

### P1 级别（中危修复）
- ✅ **浏览器并发限制** - Semaphore 控制最多 3 个并发
- ✅ **API 频率限制** - 至少间隔 1 秒调用
- ✅ **超时控制** - 浏览器 30 秒/GitHub API 10 秒超时

### P2 级别（低危修复）
- ✅ **错误处理优化** - 不泄露敏感信息
- ✅ **日志记录** - 记录安全事件
- ✅ **环境变量配置** - 可自定义安全参数

---

## 📋 安装说明

### 快速安装
```bash
clawhub install github-reader
```

### 手动安装
```bash
git clone https://github.com/your-repo/github-reader-skill.git
cd github-reader-skill
./install_v3_secure.sh
```

### 配置环境变量（可选）
```bash
# .bashrc 或 .zshrc
export GITVIEW_CACHE_TTL="12"          # 缓存时间（小时）
export GITVIEW_MAX_BROWSER="2"         # 最大并发浏览器
export GITVIEW_GITHUB_DELAY="2.0"      # API 调用间隔（秒）
```

---

## 💡 使用示例

### 基础用法
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

> **分析时间**: 2026-03-13 00:30  
> **数据来源**: Zread + GitHub API + 技术社区

---

## 💡 一句话介绍
BitNet.cpp 是微软官方推出的 1 比特量化大语言模型推理框架...

## 📊 项目卡片
| 指标 | 值 |
|------|-----|
| ⭐ Stars | 12.5k |
| 🍴 Forks | 2.1k |
| 📝 Issues | 156 |
| 🐍 语言 | Python |
| 📄 许可证 | MIT |

## 🔗 快速链接
| 平台 | 链接 |
|------|------|
| GitHub | https://github.com/microsoft/BitNet |
| Zread | https://zread.ai/microsoft/BitNet |
| GitView | http://localhost:8080/?repo=microsoft/BitNet |

...（完整报告包含架构、性能、竞品、使用指南等）
```

---

## ⚙️ 技术栈

- **语言**: Python 3.9+
- **依赖**: OpenClaw compatible platform
- **工具**: web_fetch, browser
- **缓存**: 文件系统缓存（JSON 格式）
- **并发**: asyncio 异步编程

---

## 🔒 安全审计

### 已通过测试
- ✅ 输入验证测试（路径遍历、特殊字符）
- ✅ URL 注入测试（SSRF 防护）
- ✅ 缓存投毒测试（数据验证）
- ✅ 并发压力测试（100 次请求）
- ✅ 超时控制测试（网络延迟模拟）

### 已知限制
- ⚠️ 依赖 Zread 网站可用性
- ⚠️ GitHub API 未认证时配额有限（60 次/小时）
- ⚠️ 浏览器资源占用（每个请求约 50MB 内存）

---

## 📈 性能指标

| 场景 | 耗时 | 备注 |
|------|------|------|
| 首次分析 | 10-15 秒 | 抓取 + 分析 |
| 缓存命中 | < 1 秒 | 直接返回 |
| 缓存过期 | 12-24 小时 | 可配置 |
| 并发限制 | 最多 3 个 | 浏览器 |
| API 限流 | 1 次/秒 | GitHub |

---

## 🐛 已知问题

1. **Zread 动态渲染** - 需要浏览器抓取（8-10 秒）
   -  workaround: 使用缓存减少重复抓取

2. **GitHub API 限流** - 未认证只有 60 次/小时
   -  workaround: 配置 `GITHUB_TOKEN` 环境变量

3. **大项目分析慢** - 超过 10k 文件的项目可能超时
   -  workaround: 增加 `GITVIEW_BROWSER_TIMEOUT` 配置

---

## 🚀 路线图

### v3.1（计划中）
- [ ] 支持私有仓库（GitHub Token）
- [ ] 添加搜索 API 集成
- [ ] PDF/Markdown 导出功能

### v3.2（计划中）
- [ ] 批量分析多个项目
- [ ] 生成对比报告
- [ ] 推荐最佳选择

### v4.0（未来）
- [ ] 实时 GitHub 趋势分析
- [ ] 技术社区评价聚合
- [ ] AI 驱动的深度洞察

---

## 📞 支持与反馈

- **问题反馈**: https://github.com/your-repo/github-reader-skill/issues
- **讨论区**: https://github.com/your-repo/github-reader-skill/discussions
- **文档**: https://github.com/your-repo/github-reader-skill/wiki

---

## 📄 许可证

MIT License

---

## 👨‍💻 作者

**虾软** 🦐
- GitHub: @your-github-id
- 龙虾团队 - 专业软件工程师

---

## 🙏 致谢

- [Zread](https://zread.ai) - 深度代码解读
- [GitHub API](https://docs.github.com/en/rest) - 项目数据
- [OpenClaw](https://openclaw.ai) - Skill 框架

---

*最后更新：2026-03-13*  
*版本：v3.0（安全加固版）*
