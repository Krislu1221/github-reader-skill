"""
GitHub Reader Skill — 自动解读 GitHub 项目
"""

__version__ = "3.1.4"

from .github_reader_v3_secure import (
    SecureGitHubReaderV3,
    GitHubAPIClient,
    SecureGitHubReaderCache,
    SecurityConfig,
    validate_repo_name,
    safe_url_join,
    safe_file_path,
    run,
)

__all__ = [
    "SecureGitHubReaderV3",
    "GitHubAPIClient",
    "SecureGitHubReaderCache",
    "SecurityConfig",
    "validate_repo_name",
    "safe_url_join",
    "safe_file_path",
    "run",
    "__version__",
]
