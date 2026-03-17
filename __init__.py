"""
GitHub Reader Skill - 自动解读 GitHub 项目

用法：
  /github-read owner/repo
  或发送 GitHub URL 自动触发
"""

import re
from nanobot.agent.skill import Skill
from nanobot.agent.tools.registry import tool


class GitHubReaderSkill(Skill):
    """GitHub 项目解读 Skill"""
    
    name = "github-reader"
    description = "解读 GitHub 项目，生成结构化报告"
    
    # 触发模式
    triggers = [
        r'/github-read\s+([^\s]+)',
        r'解读 (?:这个 | 这) 仓库 [:：]?\s*(https?://github\.com/[^\s]+)',
        r'分析 (?:这个 | 这) 项目 [:：]?\s*(https?://github\.com/[^\s]+)',
    ]
    
    async def execute(self, context: dict) -> str:
        """执行技能"""
        
        message = context.get('message', '')
        
        # 解析 GitHub URL 或 owner/repo
        target = self.extract_target(message)
        if not target:
            return "❌ 未找到有效的 GitHub 链接\n\n请提供类似以下格式：\n- https://github.com/owner/repo\n- owner/repo"
        
        owner, repo = target
        
        # 生成报告
        report = await self.generate_report(owner, repo)
        
        return report
    
    def extract_target(self, message: str) -> tuple[str, str] | None:
        """从消息中提取 GitHub 目标"""
        
        patterns = [
            r'github\.com/([^/]+)/([^/\s?]+)',  # 完整 URL
            r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_.-]+)$',  # owner/repo
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                return match.group(1), match.group(2)
        
        return None
    
    async def generate_report(self, owner: str, repo: str) -> str:
        """生成项目解读报告"""
        
        # 生成链接
        github_url = f'https://github.com/{owner}/{repo}'
        zread_url = f'https://zread.ai/{owner}/{repo}'
        gitview_url = f'http://localhost:8080/?repo={owner}/{repo}'
        
        # 尝试获取真实数据（调用 GitHub API）
        repo_info = await self.fetch_github_info(owner, repo)
        
        # 构建报告
        report = f"""
# 📦 {owner}/{repo} 项目解读

## 🔗 快速链接
| 平台 | 链接 | 说明 |
|------|------|------|
| **GitHub** | {github_url} | 源代码仓库 |
| **Zread** | {zread_url} | 📖 深度解读（推荐） |
| **GitView** | {gitview_url} | 🚀 快速概览 |

## 📊 项目卡片
"""
        
        # 添加项目信息
        if repo_info:
            report += f"""
- ⭐ **Stars**: {repo_info.get('stars', 'N/A')}
- 🍴 **Forks**: {repo_info.get('forks', 'N/A')}
- 📝 **Issues**: {repo_info.get('issues', 'N/A')}
- 🐍 **语言**: {repo_info.get('language', 'N/A')}
- 📄 **许可证**: {repo_info.get('license', 'N/A')}
- 🕐 **最后更新**: {repo_info.get('updated', 'N/A')}
"""
        
        report += f"""

## 💡 核心价值
> {repo_info.get('description', '该项目致力于解决开发过程中的效率问题，提供自动化和智能化的解决方案。') if repo_info else '这是一个开源项目，提供便捷的开发工具和自动化解决方案。'}

## 🎯 主要功能
（从 Zread 获取详细功能列表）

## 🏗️ 架构亮点
（从 Zread 获取架构解析）

## 🚀 快速开始
```bash
# 克隆项目
git clone {github_url}.git
cd {repo}

# 查看 README 获取详细安装指南
```

## 📖 建议阅读顺序

1. **快速了解** → 使用 [GitView]({gitview_url}) 查看项目概况（30 秒）
2. **深度解读** → 阅读 [Zread]({zread_url}) 完整架构和代码解析（5 分钟）
3. **动手实践** → 在 GitHub 查看 README 和文档
4. **社区互动** → 浏览 Issues 和 Discussions

---
*由 Krislu + 🦐 虾软 生成*
"""
        
        return report
    
    async def fetch_github_info(self, owner: str, repo: str) -> dict | None:
        """从 GitHub API 获取项目信息"""
        try:
            # 使用 nanobot 的 web_fetch 工具
            from nanobot.agent.tools.web import web_fetch
            
            api_url = f'https://api.github.com/repos/{owner}/{repo}'
            response = await web_fetch(api_url)
            
            if response:
                data = json.loads(response)
                return {
                    'stars': self.format_number(data.get('stargazers_count', 0)),
                    'forks': self.format_number(data.get('forks_count', 0)),
                    'issues': data.get('open_issues_count', 0),
                    'language': data.get('language', 'Unknown'),
                    'license': data.get('license', {}).get('spdx_id', 'Unknown') if data.get('license') else 'Unknown',
                    'description': data.get('description', ''),
                    'updated': self.relative_time(data.get('pushed_at', ''))
                }
        except Exception as e:
            print(f"获取 GitHub 信息失败：{e}")
        
        return None
    
    def format_number(self, num: int) -> str:
        """格式化数字（如 1.2k）"""
        if num >= 1000000:
            return f'{num / 1000000:.1f}M'
        elif num >= 1000:
            return f'{num / 1000:.1f}k'
        return str(num)
    
    def relative_time(self, date_str: str) -> str:
        """转换为相对时间"""
        from datetime import datetime
        
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


# 注册 Skill
def register():
    return GitHubReaderSkill()
