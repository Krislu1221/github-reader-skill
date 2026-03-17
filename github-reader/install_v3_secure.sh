#!/bin/bash

# GitHub Reader Skill v3.1（国际化安全加固版）安装脚本
# GitHub Reader Skill v3.1 (International Security Hardened) Installation Script

set -e  # 遇到错误立即退出 / Exit on error

echo "🦐 安装 GitHub Reader Skill v3.1（国际化安全加固版）..."
echo "🦐 Installing GitHub Reader Skill v3.1 (International Security Hardened)..."
echo ""

# 使用环境变量或 OpenClaw 默认路径 / Use environment variable or OpenClaw default
SKILL_DIR="${GITVIEW_SKILL_DIR:-$HOME/.openclaw/skills/github-reader}"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

# 创建目录 / Create directories
mkdir -p "$SKILL_DIR"
mkdir -p /tmp/gitview_cache

# 复制文件 / Copy files
echo "📦 复制文件... / Copying files..."
cp "$SOURCE_DIR/__init__.py" "$SKILL_DIR/"
cp "$SOURCE_DIR/github_reader_v3_secure.py" "$SKILL_DIR/"
cp "$SOURCE_DIR/SECURITY.md" "$SKILL_DIR/"
cp "$SOURCE_DIR/SKILL.md" "$SKILL_DIR/"
cp "$SOURCE_DIR/README_BILINGUAL.md" "$SKILL_DIR/"
cp "$SOURCE_DIR/clawhub.json" "$SKILL_DIR/"

# 设置权限 / Set permissions
chmod 700 /tmp/gitview_cache  # 仅所有者可访问 / Owner access only
chmod +x "$SKILL_DIR"/*.py 2>/dev/null || true

echo "✅ Skill 已安装到：$SKILL_DIR"
echo "✅ Skill installed to: $SKILL_DIR"
echo "✅ 缓存目录：/tmp/gitview_cache（权限：700）"
echo "✅ Cache directory: /tmp/gitview_cache (permission: 700)"
echo ""

echo "🛡️ 安全特性 / Security Features:"
echo "  ✅ P0: 输入验证（防止 URL 注入）/ Input validation (Prevents URL injection)"
echo "  ✅ P0: 安全 URL 拼接（防止 SSRF）/ Safe URL joining (Prevents SSRF)"
echo "  ✅ P0: 缓存数据验证（防止投毒）/ Cache validation (Prevents poisoning)"
echo "  ✅ P0: 路径安全检查（防止遍历）/ Path security check (Prevents traversal)"
echo "  ✅ P1: 浏览器并发限制 / Browser concurrency limit"
echo "  ✅ P1: API 频率限制 / API rate limiting"
echo "  ✅ P1: 超时控制 / Timeout control"
echo ""

echo "⚙️ 环境变量（可选配置）/ Environment Variables (Optional):"
echo "  export GITVIEW_CACHE_TTL=\"12\"          # 缓存时间（小时）/ Cache TTL (hours)"
echo "  export GITVIEW_MAX_BROWSER=\"2\"         # 最大并发浏览器 / Max concurrent browsers"
echo "  export GITVIEW_GITHUB_DELAY=\"2.0\"      # API 调用间隔（秒）/ API call delay (seconds)"
echo ""

echo "⏱️ 性能指标 / Performance Metrics:"
echo "  - 首次分析 / First analysis: 10-15 秒 / seconds"
echo "  - 缓存命中 / Cache hit: < 1 秒 / second"
echo "  - 缓存过期 / Cache expiry: 12-24 小时 / hours (configurable)"
echo ""

echo "📊 安全审计 / Security Audit:"
echo "  ✅ 所有输入都经过验证 / All inputs validated"
echo "  ✅ URL 拼接使用安全函数 / Safe URL joining"
echo "  ✅ 缓存数据有大小限制 / Cache size limits"
echo "  ✅ 文件路径经过规范化 / Path normalization"
echo "  ✅ 有并发和超时控制 / Concurrency and timeout control"
echo "  ✅ 错误不会泄露敏感信息 / Error handling (no info leakage)"
echo ""

echo "💡 用法 / Usage:"
echo "  /github-read microsoft/BitNet"
echo "  或 / or: 发送 GitHub URL 自动触发 / Send GitHub URL to auto-trigger"
echo ""

echo "🔄 重启 gateway 使 Skill 生效：/ Restart gateway to apply Skill:"
echo "  openclaw gateway restart"
echo ""

echo "🔒 查看安全文档：/ View security documentation:"
echo "  cat \$SKILL_DIR/SECURITY.md"
echo "  cat \$SKILL_DIR/SKILL.md  # 中英双语 / Bilingual"
echo ""

echo "✅ 安装完成！/ Installation complete!"
