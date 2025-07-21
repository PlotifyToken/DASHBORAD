# 🚨 部署故障排除指南

网站打不开？按照这个步骤排查！

## 🔍 当前问题：404 DEPLOYMENT_NOT_FOUND

这说明Vercel没有找到你的部署。

## 🛠️ 解决步骤

### 第1步：检查Vercel项目

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 查看是否有 `DASHBORAD` 项目
3. 如果没有，说明导入失败

### 第2步：重新导入项目

如果项目不存在：

1. 在Vercel点击 **"New Project"**
2. 选择 **"Import Git Repository"** 
3. 输入：`https://github.com/PlotifyToken/DASHBORAD`
4. 点击 **"Import"**

### 第3步：配置环境变量 🔑

**在 Settings → Environment Variables 添加：**

```
CUSTOMER_IO_APP_API_KEY = 4da41dd5d42c3edb11415201fc1c024a
REVENUECAT_TOKEN = sk_EWEOIOZJEmiXoDOMkywmrklkuLwXi
```

### 第4步：检查部署日志

1. 在Vercel项目页面点击 **"Functions"**
2. 查看是否有部署错误
3. 检查 `api/data.py` 是否正确构建

### 第5步：手动触发重新部署

1. 在项目设置中点击 **"Deployments"**
2. 点击 **"Redeploy"**

## 🔧 常见问题

### 问题1：项目导入失败
**解决**：确保GitHub仓库是public或已授权Vercel访问

### 问题2：环境变量未设置
**解决**：必须设置API密钥，否则API会返回500错误

### 问题3：Python函数构建失败
**解决**：检查 `requirements.txt` 是否包含 `requests`

### 问题4：路由配置错误
**解决**：`vercel.json` 应该包含正确的路由配置

## 🧪 部署成功验证

部署成功后，以下链接应该有响应：

- **主页**：`https://unlockland.vercel.app/`
- **API**：`https://unlockland.vercel.app/api/data`

预期API响应：
```json
{
  "totalUsers": 376,
  "activeSubscriptions": 4,
  "arr": 48.0,
  "sources": {
    "customerIO": "real_data",
    "revenueCat": "real_data"
  }
}
```

## 📞 如果还是不行

1. 检查Vercel项目设置
2. 确认GitHub仓库连接正常
3. 查看部署日志详细错误
4. 尝试删除项目重新导入

## ⚡ 快速重新部署命令

如果你想更新代码：

```bash
git add .
git commit -m "Fix deployment issues"
git push origin main
```

Vercel会自动重新部署。 