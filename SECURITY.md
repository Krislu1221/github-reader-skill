# GitHub Reader Skill Security Guide

**GitHub Reader Skill 安全配置指南**

---

## 🔒 Security Features / 安全特性

v3.1 Security Hardened Version has fixed the following security issues:  
v3.1 安全加固版已修复以下安全问题：

### P0 Level (Critical Fixes) / P0 级别（高危修复）

- ✅ **Input Validation** / **输入验证** - Prevents URL injection / 防止 URL 注入
- ✅ **Safe URL Joining** / **安全 URL 拼接** - Prevents SSRF attacks / 防止 SSRF 攻击
- ✅ **Cache Data Validation** / **缓存数据验证** - Prevents poisoning / 防止投毒
- ✅ **Path Security Check** / **路径安全检查** - Prevents traversal / 防止遍历

### P1 Level (Medium Fixes) / P1 级别（中危修复）

- ✅ **Browser Concurrency Limit** / **浏览器并发限制**
- ✅ **API Rate Limiting** / **API 频率限制**
- ✅ **Timeout Control** / **超时控制**

### P2 Level (Low Fixes) / P2 级别（低危修复）

- ✅ **Error Handling Optimization** / **错误处理优化**
- ✅ **Logging** / **日志记录**
- ✅ **Environment Variable Configuration** / **环境变量配置**

---

## ⚙️ Security Configuration / 安全配置

### Environment Variables / 环境变量

```bash
# Cache Configuration / 缓存配置
export GITVIEW_CACHE_DIR="/tmp/gitview_cache"  # Cache directory / 缓存目录
export GITVIEW_CACHE_TTL="24"                   # Cache TTL (hours) / 缓存时间（小时）
export GITVIEW_CACHE_MAX_SIZE="1"               # Max cache file (MB) / 最大缓存文件（MB）

# Performance Configuration / 性能配置
export GITVIEW_MAX_BROWSER="3"                  # Max concurrent browsers / 最大并发浏览器数
export GITVIEW_GITHUB_DELAY="2.0"               # API call delay (seconds) / API 调用间隔（秒）

# Timeout Configuration / 超时配置
export GITVIEW_BROWSER_TIMEOUT="30"             # Browser timeout (seconds) / 浏览器超时（秒）
export GITVIEW_GITHUB_TIMEOUT="10"              # GitHub API timeout (seconds) / GitHub API 超时（秒）
```

---

## 🔍 Security Testing / 安全测试

### Test Cases / 测试用例

```bash
# 1. Normal request / 正常请求
/github-read microsoft/BitNet
# ✅ Should succeed / 应该成功

# 2. Path traversal attempt / 路径遍历尝试
/github-read ../etc/passwd
# ❌ Should be rejected / 应该拒绝

# 3. Special character attempt / 特殊字符尝试
/github-read user%20name/repo
# ❌ Should be rejected / 应该拒绝

# 4. Long name attempt / 超长名称尝试
/github-read a{150 characters}/repo
# ❌ Should be rejected (>100 characters) / 应该拒绝（>100 字符）

# 5. Concurrency stress test / 并发压力测试
# Send 10 requests simultaneously / 同时发送 10 个请求
# ✅ Should limit to max 3 concurrent / 应该限制为最多 3 个并发

# 6. Timeout test / 超时测试
# Simulate 60s network delay / 模拟网络延迟 60 秒
# ✅ Should timeout after 30s / 应该 30 秒后超时返回
```

---

## 🚨 Emergency Response / 应急响应

### If Security Issue Occurs / 如果发生安全问题

1. **Stop Skill Immediately** / **立即停止 Skill**
   ```bash
   openclaw gateway stop
   ```

2. **Clear Cache** / **清理缓存**
   ```bash
   rm -rf /tmp/gitview_cache
   ```

3. **Check Logs** / **检查日志**
   ```bash
   tail -n 100 ~/.openclaw/logs/gateway.log
   ```

4. **Update to Latest Version** / **更新到最新版本**
   ```bash
   clawhub update github-reader
   ```

---

## ✅ Security Checklist / 安全检查清单

Before publishing, confirm / 发布前确认：

- [x] All inputs are validated / 所有输入都经过验证
- [x] URL joining uses safe functions / URL 拼接使用安全函数
- [x] Cache data has size limits / 缓存数据有大小限制
- [x] File paths are normalized / 文件路径经过规范化
- [x] Concurrency and timeout control / 有并发和超时控制
- [x] Errors don't leak sensitive information / 错误不会泄露敏感信息
- [x] Logging security events / 日志记录安全事件
- [x] Environment variables are configurable / 环境变量可配置

---

## 📊 Security Audit Results / 安全审计结果

### Passed Tests / 已通过测试

- ✅ Input validation tests (path traversal, special characters) / 输入验证测试（路径遍历、特殊字符）
- ✅ URL injection tests (SSRF protection) / URL 注入测试（SSRF 防护）
- ✅ Cache poisoning tests (data validation) / 缓存投毒测试（数据验证）
- ✅ Concurrency stress tests (100 requests) / 并发压力测试（100 次请求）
- ✅ Timeout control tests (network latency simulation) / 超时控制测试（网络延迟模拟）

---

## 📚 References / 参考资料

- [OWASP Input Validation](https://owasp.org/www-community/controls/Input_Validation)
- [OWASP SSRF Prevention](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery)
- [Python Security Best Practices](https://docs.python.org/3/library/security.html)

---

*Version / 版本: v3.1 (Security Hardened / 安全加固版)*  
*Last Updated / 最后更新: 2026-03-13*
