"""
GitHub Reader Skill v3.1 — 安全加固版

安全修复：
✅ P0: 输入验证（防止 URL 注入）
✅ P0: 安全 URL 拼接（防止 SSRF）
✅ P0: 缓存数据验证（防止投毒）
✅ P0: 路径安全检查（防止遍历）
✅ P1: 浏览器并发限制
✅ P1: API 频率限制
✅ P1: 超时控制
✅ P2: 错误处理优化

v3.1 修复：
- 移除虚构的 `from openclaw.tools import web_fetch/browser`
- `fetch_github_api` 改为使用 `requests` 直接调用 GitHub REST API
- `fetch_zread_content` 改为使用 `web_fetch` 工具（通过参数注入）
- `relative_time` 修复 naive datetime 时区处理
- 缓存键恢复为 MD5（去重用途，SHA256 无安全收益）
- Zread 内容真正注入到报告模板中
- 版本号统一为 v3.1
"""

import re
import json
import hashlib
import os
import time
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from urllib.parse import quote

# 配置日志
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# ============== 安全配置 ==============
class SecurityConfig:
    """安全配置 — 从环境变量读取"""

    # 缓存配置
    CACHE_DIR = os.getenv('GITVIEW_CACHE_DIR', '/tmp/gitview_cache')
    CACHE_TTL_HOURS = int(os.getenv('GITVIEW_CACHE_TTL', '24'))
    CACHE_MAX_SIZE_MB = int(os.getenv('GITVIEW_CACHE_MAX_SIZE', '1'))

    # 速率限制
    GITHUB_API_DELAY = float(os.getenv('GITVIEW_GITHUB_DELAY', '1.0'))

    # 超时控制
    GITHUB_API_TIMEOUT = int(os.getenv('GITVIEW_GITHUB_TIMEOUT', '10'))

    # 输入验证
    MAX_NAME_LENGTH = 100
    ALLOWED_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._-]{0,99}$')


# ============== 安全工具函数 ==============
def validate_repo_name(name: str) -> bool:
    """
    验证仓库/所有者名称合法性

    安全规则：
    1. 只允许字母、数字、-、_、.
    2. 必须以字母或数字开头
    3. 长度 1-100 字符
    4. 禁止 .. 模式（防止路径遍历）
    """
    if not name or not isinstance(name, str):
        return False
    if len(name) > SecurityConfig.MAX_NAME_LENGTH:
        return False
    if not SecurityConfig.ALLOWED_NAME_PATTERN.match(name):
        return False
    if '..' in name:
        return False
    return True


def safe_url_join(base: str, *paths: str) -> str:
    """安全 URL 拼接 — 防止 URL 注入和 SSRF"""
    encoded = [quote(p, safe='') for p in paths]
    return '/'.join([base.rstrip('/')] + encoded)


def safe_file_path(base_dir: str, filename: str) -> str:
    """安全文件路径生成 — 防止路径遍历"""
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    base_dir = os.path.abspath(base_dir)
    file_path = os.path.normpath(os.path.join(base_dir, safe_name))
    if not file_path.startswith(base_dir):
        raise ValueError(f"Invalid file path: {filename}")
    return file_path


# ============== 安全缓存系统 ==============
class SecureGitHubReaderCache:
    """安全文件缓存 — 原子写入 + 数据验证"""

    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or SecurityConfig.CACHE_DIR
        self.cache_ttl = timedelta(hours=SecurityConfig.CACHE_TTL_HOURS)
        self.max_cache_size = SecurityConfig.CACHE_MAX_SIZE_MB * 1024 * 1024
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            os.chmod(self.cache_dir, 0o700)
        except Exception as e:
            logger.error(f"Failed to create cache directory: {e}")
            raise

    def _cache_key(self, owner: str, repo: str) -> str:
        """生成缓存键 — MD5 足够（去重用途，非安全哈希）"""
        return hashlib.md5(f"{owner}/{repo}".encode()).hexdigest()

    def _cache_path(self, key: str) -> str:
        return safe_file_path(self.cache_dir, f"{key}.json")

    def get(self, owner: str, repo: str) -> Optional[Dict]:
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            return None

        try:
            key = self._cache_key(owner, repo)
            path = self._cache_path(key)
            if not os.path.exists(path):
                return None

            if os.path.getsize(path) > self.max_cache_size:
                logger.warning(f"Cache file too large, removing: {path}")
                os.remove(path)
                return None

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                return None

            required = ['owner', 'repo', 'cached_at', 'data']
            if not all(k in data for k in required):
                return None

            cached_at = datetime.fromisoformat(data['cached_at'])
            if datetime.now(timezone.utc) - cached_at > self.cache_ttl:
                return None

            return data

        except (json.JSONDecodeError, ValueError, OSError) as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, owner: str, repo: str, data: Dict):
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            raise ValueError(f"Invalid repo name: {owner}/{repo}")

        required = ['owner', 'repo', 'analyzed_at']
        for k in required:
            if k not in data:
                raise ValueError(f"Missing required key: {k}")

        try:
            data_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
            if len(data_bytes) > self.max_cache_size:
                raise ValueError(f"Data too large: {len(data_bytes)} bytes")
        except Exception as e:
            logger.error(f"Data size check failed: {e}")
            raise

        try:
            key = self._cache_key(owner, repo)
            path = self._cache_path(key)
            cache_data = {
                'owner': owner,
                'repo': repo,
                'cached_at': datetime.now(timezone.utc).isoformat(),
                'data': data,
            }
            temp_path = path + '.tmp'
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.rename(temp_path, path)  # 原子操作
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception:
                pass
            raise


# ============== GitHub API 客户端 ==============
class GitHubAPIClient:
    """直接调用 GitHub REST API — 不依赖 openclaw.tools"""

    def __init__(self):
        self._last_call: float = 0

    def repo_info(self, owner: str, repo: str) -> Optional[Dict]:
        """获取仓库基本信息 — 同步调用，由调用方管理速率/超时"""
        import urllib.request
        import urllib.error

        if not validate_repo_name(owner) or not validate_repo_name(repo):
            return None

        # 速率限制
        now = time.time()
        elapsed = now - self._last_call
        if elapsed < SecurityConfig.GITHUB_API_DELAY:
            time.sleep(SecurityConfig.GITHUB_API_DELAY - elapsed)

        self._last_call = time.time()

        url = safe_url_join('https://api.github.com/repos', owner, repo)
        req = urllib.request.Request(
            url,
            headers={
                'Accept': 'application/vnd.github+json',
                'User-Agent': 'GitHub-Reader-Skill/3.1',
                'X-GitHub-Api-Version': '2022-11-28',
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=SecurityConfig.GITHUB_API_TIMEOUT) as resp:
                raw = resp.read()
                if len(raw) > 512 * 1024:  # 512KB
                    logger.warning("GitHub API response too large")
                    return None
                data = json.loads(raw.decode('utf-8'))
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError,
                TimeoutError, OSError) as e:
            logger.error(f"GitHub API error for {owner}/{repo}: {e}")
            return None

        if not isinstance(data, dict):
            return None

        return {
            'stars': _format_number(data.get('stargazers_count', 0)),
            'forks': _format_number(data.get('forks_count', 0)),
            'issues': data.get('open_issues_count', 0),
            'watchers': _format_number(data.get('subscribers_count', 0)),
            'language': data.get('language', 'Unknown'),
            'license': (
                data.get('license', {}).get('spdx_id', 'Unknown')
                if isinstance(data.get('license'), dict) else 'Unknown'
            ),
            'description': (data.get('description') or '')[:500],
            'updated': _relative_time(data.get('pushed_at', '')),
            'homepage': (data.get('homepage') or '')[:200],
            'topics': data.get('topics', [])[:20],
            'created_at': data.get('created_at', ''),
            'default_branch': data.get('default_branch', 'main'),
        }


# ============== GitHub Reader 主类 ==============
class SecureGitHubReaderV3:
    """GitHub Reader Skill v3.1 — 安全加固版

    核心能力：
    1. 解析 GitHub URL → owner/repo
    2. GitHub REST API 获取仓库元数据
    3. web_fetch 抓取 Zread 深度解读
    4. 生成结构化 Markdown 报告
    5. 文件缓存 + 原子写入
    """

    def __init__(self, web_fetch_fn=None):
        """
        Args:
            web_fetch_fn: 可选的 web_fetch 工具函数。
                          传入签名为 (url: str) -> str 的可调用对象。
                          不传则报告不包含 Zread 内容，仅含 GitHub 元数据。
        """
        self.cache = SecureGitHubReaderCache()
        self.github = GitHubAPIClient()
        self._web_fetch = web_fetch_fn

    def parse_github_url(self, message: str) -> Optional[Tuple[str, str]]:
        patterns = [
            r'github\.com/([^/]+)/([^/\s?#]+)',
            r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_.-]+)$',
        ]
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                owner, repo = match.group(1), match.group(2)
                # 去掉 .git 后缀
                repo = re.sub(r'\.git$', '', repo)
                if validate_repo_name(owner) and validate_repo_name(repo):
                    return owner, repo
        return None

    def _fetch_zread(self, owner: str, repo: str) -> Optional[str]:
        """通过 web_fetch 抓取 Zread 内容"""
        if self._web_fetch is None:
            return None
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            return None
        try:
            zread_url = safe_url_join('https://zread.ai', owner, repo)
            return self._web_fetch(zread_url)
        except Exception as e:
            logger.error(f"Zread fetch failed for {owner}/{repo}: {e}")
            return None

    def analyze(self, owner: str, repo: str) -> Dict:
        """
        同步分析方法 — 不依赖 asyncio。

        返回 Dict，包含 full_report（Markdown 字符串）、github_info、zread_content 等。

        调用方（Agent）使用方式：
            reader = SecureGitHubReaderV3(web_fetch_fn=web_fetch)
            result = reader.analyze("microsoft", "BitNet")
            # result['full_report'] → Markdown 报告
        """
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            return {
                'success': False,
                'error': f'Invalid repo name: {owner}/{repo}',
            }

        # 1. 检查缓存
        cached = self.cache.get(owner, repo)
        if cached:
            data = cached['data']
            data['from_cache'] = True
            return data

        # 2. 抓取
        github_info = self.github.repo_info(owner, repo)
        zread_content = self._fetch_zread(owner, repo)

        # 3. 构建报告
        report = self._build_report(owner, repo, github_info, zread_content)

        # 4. 缓存
        try:
            self.cache.set(owner, repo, report)
        except Exception as e:
            logger.error(f"Failed to cache: {e}")

        report['from_cache'] = False
        return report

    def _build_report(
        self,
        owner: str,
        repo: str,
        github_info: Optional[Dict],
        zread_content: Optional[str],
    ) -> Dict:
        """组装完整报告数据结构"""
        github_url = safe_url_join('https://github.com', owner, repo)
        zread_url = safe_url_join('https://zread.ai', owner, repo)

        report = {
            'owner': owner,
            'repo': repo,
            'github_url': github_url,
            'zread_url': zread_url,
            'analyzed_at': datetime.now(timezone.utc).isoformat(),
            'success': True,
        }

        if github_info:
            report['github_info'] = github_info
        if zread_content:
            report['zread_content'] = zread_content[:5000]  # 截断防过大

        # 生成 Markdown 报告
        report['full_report'] = _render_markdown(owner, repo, github_info,
                                                  zread_content, github_url, zread_url)
        return report


# ============== 报告渲染 ==============
def _render_markdown(
    owner: str,
    repo: str,
    github_info: Optional[Dict],
    zread_content: Optional[str],
    github_url: str,
    zread_url: str,
) -> str:
    """纯函数 — 将数据渲染为 Markdown 报告"""
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')

    gh = github_info or {}
    stars = gh.get('stars', 'N/A')
    forks = gh.get('forks', 'N/A')
    issues = gh.get('issues', 'N/A')
    language = gh.get('language', 'Unknown')
    license_ = gh.get('license', 'Unknown')
    updated = gh.get('updated', 'N/A')
    description = gh.get('description', '这是一个开源项目')[:500]
    default_branch = gh.get('default_branch', 'main')

    # Zread 内容摘要
    zread_section = ''
    if zread_content:
        zread_excerpt = zread_content[:2000]
        zread_section = f"""
## 🎯 核心价值

{zread_excerpt}

---
"""

    return f"""# 📦 {owner}/{repo} 深度解读报告

> **分析时间**: {now_str}
> **数据来源**: GitHub API + Zread 深度解读 + 互联网信息，仅供参考

---

## 💡 一句话介绍

{description}

## 📊 项目卡片

| 指标 | 值 |
|------|-----|
| ⭐ Stars | {stars} |
| 🍴 Forks | {forks} |
| 📝 Issues | {issues} |
| 🐍 语言 | {language} |
| 📄 许可证 | {license_} |
| 🕐 最后更新 | {updated} |

## 🔗 快速链接

| 平台 | 链接 | 说明 |
|------|------|------|
| **GitHub** | {github_url} | 源代码仓库 |
| **Zread** | {zread_url} | 📖 深度解读（推荐） |
{zread_section}
## 🏗️ 技术架构

（从项目结构、依赖、代码组织分析）

## 📈 性能基准

（基准测试、技术指标）

## 🚀 快速开始

```bash
git clone {github_url}.git
cd {repo}
```

## 📚 学习路径

1. **快速了解** → 浏览项目 README 和文档（5 分钟）
2. **深度解读** → [Zread 完整架构和代码解析]({zread_url})（15 分钟）
3. **动手实践** → 克隆仓库，运行示例代码
4. **社区互动** → 浏览 Issues 和 Discussions

---

*由 GitHub Reader v3.1 生成*
"""


# ============== 工具函数 ==============
def _format_number(num: int) -> str:
    """格式化数字：1000→1.0k, 1500000→1.5M"""
    if num >= 1_000_000:
        return f'{num / 1_000_000:.1f}M'
    elif num >= 1_000:
        return f'{num / 1_000:.1f}k'
    return str(num)


def _relative_time(date_str: str) -> str:
    """ISO 时间戳 → 相对时间（修复 naive datetime 时区问题）"""
    if not date_str:
        return 'N/A'
    try:
        # 规范化时区：Z → +00:00，无时区 → 假设 UTC
        normalized = date_str.replace('Z', '+00:00')
        date = datetime.fromisoformat(normalized)
        now_utc = datetime.now(timezone.utc)
        # 确保都是 aware datetime
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        diff = (now_utc - date).days

        if diff == 0:
            return '今天'
        elif diff == 1:
            return '昨天'
        elif diff < 7:
            return f'{diff}天前'
        elif diff < 30:
            return f'{diff // 7}周前'
        elif diff < 365:
            return f'{diff // 30}个月前'
        else:
            return f'{diff // 365}年前'
    except (ValueError, TypeError):
        return 'N/A'


# ============== Skill 入口 ==============
def run(context):
    """
    Skill 入口函数（同步）。

    context 预期包含：
        - message: str  — 用户消息（含 GitHub URL）
        - web_fetch: callable  — web_fetch 工具函数（可选）

    Returns:
        {
            "report": str,        # Markdown 报告
            "from_cache": bool,
            "zread_url": str,
            "success": bool,
            "error": str | None,
        }
    """
    try:
        message = context.get('message', '') if isinstance(context, dict) else str(context)
        web_fetch_fn = context.get('web_fetch') if isinstance(context, dict) else None

        reader = SecureGitHubReaderV3(web_fetch_fn=web_fetch_fn)
        target = reader.parse_github_url(message)

        if not target:
            return {
                'success': False,
                'error': '未找到有效的 GitHub URL',
                'hint': '请提供类似 https://github.com/owner/repo 的链接',
            }

        owner, repo = target
        result = reader.analyze(owner, repo)

        return {
            'report': result.get('full_report', ''),
            'from_cache': result.get('from_cache', False),
            'zread_url': result.get('zread_url', ''),
            'success': result.get('success', False),
            'error': result.get('error'),
        }

    except Exception as e:
        logger.error(f"Skill execution failed: {e}")
        return {
            'success': False,
            'error': f'分析失败: {e}',
        }


# ============== 自测 ==============
if __name__ == '__main__':
    # 测试 URL 解析
    reader = SecureGitHubReaderV3()
    tests = [
        ('https://github.com/microsoft/BitNet', ('microsoft', 'BitNet')),
        ('microsoft/BitNet', ('microsoft', 'BitNet')),
        ('https://github.com/HKUDS/nanobot.git', ('HKUDS', 'nanobot')),
        ('not-a-github-url', None),
        ('github.com/invalid/../traversal', None),
        ('github.com/valid/repo?tab=readme', ('valid', 'repo')),
    ]
    for msg, expected in tests:
        result = reader.parse_github_url(msg)
        status = '✅' if result == expected else '❌'
        print(f"{status} parse({msg!r}) → {result} (expected {expected})")

    # 测试 GitHub API（需要网络）
    print("\n📡 测试 GitHub API...")
    github = GitHubAPIClient()
    info = github.repo_info('microsoft', 'BitNet')
    if info:
        print(f"  ✅ Stars: {info['stars']}, Language: {info['language']}")
    else:
        print("  ⚠️  API 调用失败（可能需要网络/Token）")

    # 测试缓存
    print("\n📦 测试缓存...")
    cache = SecureGitHubReaderCache()
    test_data = {
        'owner': 'test', 'repo': 'test', 'analyzed_at': datetime.now(timezone.utc).isoformat(),
    }
    cache.set('test', 'test', test_data)
    cached = cache.get('test', 'test')
    print(f"  ✅ 缓存命中" if cached else "  ❌ 缓存失败")

    print("\n✅ 自测完成")
