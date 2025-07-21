# 🚀 UnlockLand Dashboard 部署指南

这个指南将帮你把仪表板部署到网上，并且实现自动更新。

## 🏗️ 部署方案

我们使用 **Vercel** 平台，这样你的仪表板将：
- ✅ **自动更新数据**（每5分钟）
- ✅ **解决跨域问题**（API安全）
- ✅ **免费托管**
- ✅ **快速全球CDN**
- ✅ **HTTPS安全连接**

## 📋 部署步骤

### 1️⃣ 准备代码

确保你有以下文件：
```
├── index.html          # 主页面
├── api/
│   └── data.py         # API端点
├── vercel.json         # Vercel配置
└── requirements.txt    # Python依赖
```

### 2️⃣ 创建 GitHub 仓库

1. 去 [GitHub](https://github.com) 创建新仓库
2. 上传你的代码：

```bash
git init
git add .
git commit -m "Initial dashboard commit"
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

### 3️⃣ 部署到 Vercel

1. 去 [Vercel.com](https://vercel.com) 注册账号
2. 点击 "New Project"
3. 连接你的 GitHub 仓库
4. 选择刚创建的仓库

### 4️⃣ 配置环境变量 🔑

在 Vercel 项目设置中添加环境变量：

**Settings → Environment Variables**

添加以下变量：
```
CUSTOMER_IO_APP_API_KEY = 你的CustomerIO_API密钥
REVENUECAT_TOKEN = 你的RevenueCat_API密钥
```

### 5️⃣ 部署完成！

- Vercel会自动构建和部署
- 你会得到一个 `.vercel.app` 域名
- 例如：`https://unlockland-dashboard.vercel.app`

## 🔄 自动更新机制

### 数据更新频率
- **前端页面**：每5分钟自动刷新数据
- **API缓存**：5分钟缓存，减少API调用
- **智能更新**：页面失去焦点时暂停更新，节省资源

### 更新方式
1. **实时更新**：页面自动从你的API获取最新数据
2. **后台更新**：不需要重新部署代码
3. **错误处理**：API失败时显示错误状态

## 🔧 高级配置

### 自定义更新频率

编辑 `index.html` 中的更新间隔：
```javascript
// 每5分钟更新一次 (默认)
updateInterval = setInterval(fetchData, 5 * 60 * 1000);

// 改为每2分钟更新一次
updateInterval = setInterval(fetchData, 2 * 60 * 1000);
```

### 自定义域名

在 Vercel 项目设置中：
1. Settings → Domains
2. 添加你的自定义域名
3. 配置DNS指向Vercel

### 监控和日志

- **Vercel Analytics**：查看访问统计
- **Function Logs**：查看API调用日志
- **Error Tracking**：监控错误和性能

## 🛡️ 安全特性

### API密钥安全
- ✅ API密钥存储在服务器环境变量中
- ✅ 前端代码中看不到任何密钥
- ✅ HTTPS加密传输

### 跨域解决
- ✅ 后端API代理，无跨域问题
- ✅ 正确的CORS头配置
- ✅ 安全的API端点

## 📱 移动端支持

仪表板已优化移动端显示：
- 响应式设计
- 触摸友好
- 快速加载

## 🚨 故障排除

### 常见问题

**1. 数据显示"Error"**
- 检查环境变量是否正确设置
- 确认API密钥有效
- 查看Vercel Function日志

**2. 页面无法访问**
- 检查Vercel部署状态
- 确认DNS配置正确
- 清除浏览器缓存

**3. 数据不更新**
- 检查浏览器控制台错误
- 确认API端点正常响应
- 检查网络连接

### 获取日志

在Vercel控制台查看：
1. Functions → 点击API函数
2. 查看实时日志和错误信息

## 📞 技术支持

如果遇到问题：
1. 检查部署日志
2. 确认API密钥配置
3. 测试API端点：`https://你的域名.vercel.app/api/data`

## 🎯 下一步

部署成功后，你可以：
- 添加更多数据指标
- 设置告警和通知
- 集成其他分析工具
- 创建多个仪表板视图

---

**恭喜！🎉 你的实时仪表板现在已经上线，可以在任何地方访问，并且会自动保持数据最新！** 