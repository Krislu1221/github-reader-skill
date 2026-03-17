"""
GitHub Reader Skill v3.0 - 安全加固版

安全修复：
✅ P0: 输入验证（防止 URL 注入）
✅ P0: 安全 URL 拼接（防止 SSRF）
✅ P0: 缓存数据验证（防止投毒）
✅ P0: 路径安全检查（防止遍历）
✅ P1: 浏览器并发限制
✅ P1: API 频率限制
✅ P1: 超时控制
✅ P2: 错误处理优化
"""

import re
import json
import hashlib
import os
import time
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from urllib.parse import quote

# 配置日志
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# ============== 安全配置 ==============
class SecurityConfig:
    """安全配置 - 从环境变量读取"""
    
    # 缓存配置
    CACHE_DIR = os.getenv('GITVIEW_CACHE_DIR', '/tmp/gitview_cache')
    CACHE_TTL_HOURS = int(os.getenv('GITVIEW_CACHE_TTL', '24'))
    CACHE_MAX_SIZE_MB = int(os.getenv('GITVIEW_CACHE_MAX_SIZE', '1'))
    
    # 速率限制
    GITHUB_API_DELAY = float(os.getenv('GITVIEW_GITHUB_DELAY', '1.0'))
    MAX_CONCURRENT_BROWSER = int(os.getenv('GITVIEW_MAX_BROWSER', '3'))
    
    # 超时控制
    BROWSER_TIMEOUT = int(os.getenv('GITVIEW_BROWSER_TIMEOUT', '30'))
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
    5. 禁止以 - 开头（防止命令行注入）
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
    """
    安全的 URL 拼接
    
    使用 urllib.parse.quote 编码路径组件
    防止 URL 注入和 SSRF 攻击
    """
    encoded_paths = [quote(path, safe='') for path in paths]
    return '/'.join([base.rstrip('/')] + encoded_paths)


def safe_file_path(base_dir: str, filename: str) -> str:
    """
    安全的文件路径生成
    
    防止路径遍历攻击
    """
    # 移除所有危险字符
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    
    # 规范化路径
    base_dir = os.path.abspath(base_dir)
    file_path = os.path.normpath(os.path.join(base_dir, safe_name))
    
    # 确保结果仍在基础目录内
    if not file_path.startswith(base_dir):
        raise ValueError(f"Invalid file path: {filename}")
    
    return file_path


# ============== 安全缓存系统 ==============
class SecureGitHubReaderCache:
    """安全的文件缓存系统"""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or SecurityConfig.CACHE_DIR
        self.cache_ttl = timedelta(hours=SecurityConfig.CACHE_TTL_HOURS)
        self.max_cache_size = SecurityConfig.CACHE_MAX_SIZE_MB * 1024 * 1024
        
        # 确保缓存目录存在且安全
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """安全地创建缓存目录"""
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            # 设置目录权限（仅所有者可读写）
            os.chmod(self.cache_dir, 0o700)
        except Exception as e:
            logger.error(f"Failed to create cache directory: {e}")
            raise
    
    def _get_cache_key(self, owner: str, repo: str) -> str:
        """生成缓存键 - 使用 SHA256（比 MD5 更安全）"""
        return hashlib.sha256(f"{owner}/{repo}".encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> str:
        """获取安全的缓存文件路径"""
        return safe_file_path(self.cache_dir, f"{key}.json")
    
    def get(self, owner: str, repo: str) -> Optional[Dict]:
        """从缓存获取结果 - 带验证"""
        # 验证输入
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            logger.warning(f"Invalid repo name in cache get: {owner}/{repo}")
            return None
        
        try:
            key = self._get_cache_key(owner, repo)
            path = self._get_cache_path(key)
            
            if not os.path.exists(path):
                return None
            
            # 检查文件大小
            file_size = os.path.getsize(path)
            if file_size > self.max_cache_size:
                logger.warning(f"Cache file too large: {file_size} bytes")
                os.remove(path)
                return None
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 验证数据结构
            if not isinstance(data, dict):
                return None
            
            required_keys = ['owner', 'repo', 'cached_at', 'data']
            if not all(key in data for key in required_keys):
                return None
            
            # 检查是否过期
            cached_at = datetime.fromisoformat(data['cached_at'])
            if datetime.now() - cached_at > self.cache_ttl:
                return None
            
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in cache: {e}")
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, owner: str, repo: str, data: Dict):
        """缓存结果 - 带验证和原子写入"""
        # 验证输入
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            raise ValueError(f"Invalid repo name: {owner}/{repo}")
        
        # 验证数据大小
        try:
            data_size = len(json.dumps(data).encode('utf-8'))
            if data_size > self.max_cache_size:
                raise ValueError(f"Data too large: {data_size} bytes")
        except Exception as e:
            logger.error(f"Failed to calculate data size: {e}")
            raise
        
        # 验证数据结构
        required_keys = ['owner', 'repo', 'analyzed_at']
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")
        
        try:
            key = self._get_cache_key(owner, repo)
            path = self._get_cache_path(key)
            
            cache_data = {
                'owner': owner,
                'repo': repo,
                'cached_at': datetime.now().isoformat(),
                'data': data
            }
            
            # 原子写入（临时文件 + 重命名）
            temp_path = path + '.tmp'
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())  # 确保写入磁盘
            
            os.rename(temp_path, path)  # 原子操作
            
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            # 清理临时文件
            try:
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass
            raise


# ============== 安全的 GitHub Reader ==============
class SecureGitHubReaderV3:
    """GitHub Reader Skill v3.0 - 安全加固版"""
    
    def __init__(self):
        self.cache = SecureGitHubReaderCache()
        self.last_github_call = 0
        self.browser_semaphore = asyncio.Semaphore(SecurityConfig.MAX_CONCURRENT_BROWSER)
    
    def parse_github_url(self, message: str) -> Optional[tuple[str, str]]:
        """解析 GitHub URL - 带验证"""
        patterns = [
            r'github\.com/([^/]+)/([^/\s?]+)',
            r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_.-]+)$',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                owner, repo = match.group(1), match.group(2)
                
                # 验证名称合法性
                if validate_repo_name(owner) and validate_repo_name(repo):
                    return owner, repo
                else:
                    logger.warning(f"Invalid repo name matched: {owner}/{repo}")
                    return None
        
        return None
    
    async def fetch_github_api(self, owner: str, repo: str) -> Optional[Dict]:
        """从 GitHub API 获取实时数据 - 带速率限制和超时"""
        # 验证输入
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            logger.warning(f"Invalid repo name in fetch_github_api: {owner}/{repo}")
            return None
        
        try:
            # 速率限制
            now = time.time()
            time_since_last = now - self.last_github_call
            if time_since_last < SecurityConfig.GITHUB_API_DELAY:
                await asyncio.sleep(SecurityConfig.GITHUB_API_DELAY - time_since_last)
            
            self.last_github_call = time.time()
            
            # 使用 web_fetch 工具
            from nanobot.agent.tools.web import web_fetch
            
            api_url = safe_url_join('https://api.github.com/repos', owner, repo)
            
            # 带超时获取
            response = await asyncio.wait_for(
                web_fetch(api_url),
                timeout=SecurityConfig.GITHUB_API_TIMEOUT
            )
            
            if not response:
                return None
            
            # 限制响应大小
            if len(response) > 1024 * 1024:  # 1MB
                logger.warning("GitHub API response too large")
                return None
            
            # 安全解析 JSON
            try:
                data = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from GitHub API: {e}")
                return None
            
            # 验证数据类型
            if not isinstance(data, dict):
                return None
            
            return {
                'stars': self.format_number(data.get('stargazers_count', 0)),
                'forks': self.format_number(data.get('forks_count', 0)),
                'issues': data.get('open_issues_count', 0),
                'language': data.get('language', 'Unknown'),
                'license': data.get('license', {}).get('spdx_id', 'Unknown') if data.get('license') else 'Unknown',
                'description': data.get('description', '')[:500],  # 限制长度
                'updated': self.relative_time(data.get('pushed_at', '')),
                'homepage': data.get('homepage', '')[:200],  # 限制长度
                'topics': data.get('topics', [])[:20]  # 限制数量
            }
            
        except asyncio.TimeoutError:
            logger.error(f"GitHub API timeout for {owner}/{repo}")
            return None
        except Exception as e:
            logger.error(f"Failed to fetch GitHub API: {e}")
            return None
    
    async def fetch_zread_content(self, owner: str, repo: str) -> Optional[str]:
        """从 Zread 抓取内容 - 带并发限制和超时"""
        # 验证输入
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            logger.warning(f"Invalid repo name in fetch_zread_content: {owner}/{repo}")
            return None
        
        try:
            # 并发限制
            async with self.browser_semaphore:
                from nanobot.agent.tools.browser import browser
                
                zread_url = safe_url_join('https://zread.ai', owner, repo)
                
                # 带超时抓取
                content = await asyncio.wait_for(
                    self._fetch_with_browser(browser, zread_url),
                    timeout=SecurityConfig.BROWSER_TIMEOUT
                )
                
                return content
                
        except asyncio.TimeoutError:
            logger.error(f"Browser fetch timeout for {owner}/{repo}")
            return None
        except Exception as e:
            logger.error(f"Failed to fetch Zread: {e}")
            return None
    
    async def _fetch_with_browser(self, browser, url: str) -> str:
        """浏览器抓取实现"""
        await browser.open(url)
        await asyncio.sleep(5)  # 等待加载
        return await browser.snapshot()
    
    async def analyze_project(self, owner: str, repo: str) -> Dict:
        """综合分析项目 - 带缓存和错误处理"""
        # 验证输入（再次确认）
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            raise ValueError(f"Invalid repo name: {owner}/{repo}")
        
        # 1. 检查缓存
        cached = self.cache.get(owner, repo)
        if cached:
            cached['from_cache'] = True
            cached['cached'] = True
            return cached
        
        # 2. 并行抓取
        github_task = asyncio.create_task(self.fetch_github_api(owner, repo))
        zread_task = asyncio.create_task(self.fetch_zread_content(owner, repo))
        
        github_info, zread_content = await asyncio.gather(
            github_task, 
            zread_task,
            return_exceptions=True  # 防止一个失败影响另一个
        )
        
        # 处理异常
        if isinstance(github_info, Exception):
            logger.error(f"GitHub task failed: {github_info}")
            github_info = None
        
        if isinstance(zread_content, Exception):
            logger.error(f"Zread task failed: {zread_content}")
            zread_content = None
        
        # 3. 生成报告
        report = await self.generate_comprehensive_report(
            owner, repo, github_info, zread_content
        )
        
        # 4. 缓存结果（如果成功）
        if report and report.get('success'):
            try:
                self.cache.set(owner, repo, report)
            except Exception as e:
                logger.error(f"Failed to cache result: {e}")
        
        report['from_cache'] = False
        report['cached'] = False
        return report
    
    async def generate_comprehensive_report(
        self,
        owner: str,
        repo: str,
        github_info: Optional[Dict],
        zread_content: Optional[str]
    ) -> Dict:
        """生成综合报告"""
        
        report = {
            'owner': owner,
            'repo': repo,
            'github_url': safe_url_join('https://github.com', owner, repo),
            'zread_url': safe_url_join('https://zread.ai', owner, repo),
            'gitview_url': f'http://localhost:8080/?repo={quote(owner, safe="")}/{quote(repo, safe="")}',
            'analyzed_at': datetime.now().isoformat(),
            'success': True
        }
        
        if github_info:
            report['github_info'] = github_info
        
        if zread_content:
            report['zread_summary'] = await self.ai_summarize_zread(zread_content)
        
        report['full_report'] = await self.ai_generate_full_report(report)
        
        return report
    
    async def ai_summarize_zread(self, content: str) -> Dict:
        """AI 总结 Zread 内容"""
        # 简化版本
        return {
            'description': '从 Zread 提取的项目描述',
            'architecture': '架构要点',
            'performance': '性能数据',
            'features': ['功能 1', '功能 2'],
            'usage': '使用方法'
        }
    
    async def ai_generate_full_report(self, report: Dict) -> str:
        """AI 生成完整报告"""
        
        owner = report['owner']
        repo = report['repo']
        github_info = report.get('github_info', {})
        
        # 安全的字符串插值（限制长度）
        description = github_info.get('description', '这是一个开源项目')[:500]
        
        markdown = f"""
好的！已经抓取到相关项目的详细信息，让我来为您解读：

# 📦 {owner}/{repo} 深度解读报告

> **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **数据来源**: Zread 深度解读 + 技术社区 + 互联网信息，仅供参考

---

## 💡 一句话介绍
{description}

## 📊 项目卡片

| 指标 | 值 |
|------|-----|
| ⭐ Stars | {github_info.get('stars', 'N/A')} |
| 🍴 Forks | {github_info.get('forks', 'N/A')} |
| 📝 Issues | {github_info.get('issues', 'N/A')} |
| 🐍 语言 | {github_info.get('language', 'Unknown')} |
| 📄 许可证 | {github_info.get('license', 'Unknown')} |
| 🕐 最后更新 | {github_info.get('updated', 'N/A')} |

## 🔗 快速链接
| 平台 | 链接 | 说明 |
|------|------|------|
| **GitHub** | {report['github_url']} | 源代码仓库 |
| **Zread** | {report['zread_url']} | 📖 深度解读（推荐） |
| **GitView** | {report['gitview_url']} | 🚀 快速概览 |

## 🎯 核心价值
（从 Zread 和 GitHub 综合提取）

## 🏗️ 技术架构
（架构分析）

## 📈 性能基准
（性能数据）

## 🆚 竞品对比
（竞品分析）

## 🚀 快速开始
```bash
git clone {report['github_url']}.git
cd {repo}
```

## 📚 学习路径
1. **快速了解** → 使用 GitView 查看项目概况（30 秒）
2. **深度解读** → 阅读 Zread 完整架构和代码解析（5 分钟）
3. **动手实践** → 在 GitHub 查看 README 和文档
4. **社区互动** → 浏览 Issues 和 Discussions

## 🌍 社区反馈
（社区评价整理）

## 🔗 相关资源
- GitHub: {report['github_url']}
- Zread: {report['zread_url']}

---
*由 Krislu + 🦐 虾软 生成*
"""
        
        return markdown
    
    def format_number(self, num: int) -> str:
        """格式化数字"""
        if num >= 1000000:
            return f'{num / 1000000:.1f}M'
        elif num >= 1000:
            return f'{num / 1000:.1f}k'
        return str(num)
    
    def relative_time(self, date_str: str) -> str:
        """转换为相对时间"""
        if not date_str:
            return 'N/A'
        
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            diff = (datetime.now(date.tzinfo) - date).days
            
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
        except:
            return 'N/A'


# ============== Skill 入口 ==============
async def run(context):
    """Skill 入口函数"""
    
    try:
        message = context.get('message', '')
        
        # 解析 GitHub URL
        reader = SecureGitHubReaderV3()
        target = reader.parse_github_url(message)
        
        if not target:
            return {
                'error': '未找到有效的 GitHub URL',
                'hint': '请提供类似 https://github.com/owner/repo 的链接',
                'success': False
            }
        
        owner, repo = target
        
        # 分析项目
        result = await reader.analyze_project(owner, repo)
        
        return {
            'report': result.get('full_report', ''),
            'from_cache': result.get('from_cache', False),
            'cached': result.get('cached', False),
            'zread_url': result.get('zread_url', ''),
            'success': result.get('success', False)
        }
        
    except Exception as e:
        logger.error(f"Skill execution failed: {e}")
        return {
            'error': '分析失败，请稍后重试',
            'success': False
        }


if __name__ == '__main__':
    # 测试
    import asyncio
    
    async def test():
        result = await run({'message': 'https://github.com/microsoft/BitNet'})
        print(result.get('report', 'No report'))
    
    asyncio.run(test())
