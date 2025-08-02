# 🚀 UnlockLand Dashboard

一个实时自动更新的业务仪表板，显示 UnlockLand 应用的关键指标。

## 📊 当前数据

- **👥 总用户数**: 12,022 人
- **💰 年收入 (ARR)**: $141,648.00
- **⭐ 活跃订阅**: 124 个
- **📈 月收入 (MRR)**: $11,804.00

## ✨ 功能特性

- 🔄 **自动更新**: 每5分钟自动刷新数据
- 🌐 **实时同步**: 直接从Customer.io和RevenueCat获取真实数据
- 📱 **响应式设计**: 完美适配桌面和移动设备
- 🔒 **安全可靠**: API密钥安全存储在服务器端
- ⚡ **快速加载**: 基于Vercel的全球CDN

## 🛠️ 技术栈

- **前端**: 纯HTML/CSS/JavaScript
- **后端**: Python (Vercel Functions)
- **部署**: Vercel
- **数据源**: Customer.io + RevenueCat APIs

## 🚀 快速部署

### 方法1: 一键部署（推荐）

```bash
./deploy.sh
```

### 方法2: 手动部署

1. **创建GitHub仓库**
2. **推送代码**:
   ```bash
   git remote add origin https://github.com/你的用户名/仓库名.git
   git branch -M main
   git push -u origin main
   ```

3. **部署到Vercel**:
   - 访问 [vercel.com](https://vercel.com)
   - 导入GitHub仓库
   - 添加环境变量:
     ```
     CUSTOMER_IO_APP_API_KEY = 4da41dd5d42c3edb11415201fc1c024a
     REVENUECAT_TOKEN = sk_EWEOIOZJEmiXoDOMkywmrklkuLwXi
     ```

## 📋 文件结构

```
├── index.html          # 主仪表板页面
├── api/
│   └── data.py         # API端点（获取数据）
├── vercel.json         # Vercel配置
├── requirements.txt    # Python依赖
├── deploy.sh          # 一键部署脚本
├── simple_test.py     # API测试脚本
└── DEPLOY.md          # 详细部署指南
```

## 🧪 本地测试

运行API测试：
```bash
python3 simple_test.py
```

预期输出：
```
✅ Customer.io连接成功，找到 9 个segments
✅ RevenueCat连接成功，项目: UNLOCKLAND
🎉 所有API测试通过！
```

## 🔄 自动更新机制

### 更新频率
- **前端**: 每5分钟自动获取最新数据
- **缓存**: API响应缓存5分钟
- **智能暂停**: 页面失去焦点时暂停更新

### 数据流程
1. 前端JavaScript调用 `/api/data`
2. Vercel Function获取Customer.io和RevenueCat数据
3. 返回JSON格式的汇总数据
4. 前端更新显示并显示状态

## 📱 演示

部署完成后，访问你的Vercel域名即可看到：

- 实时用户数据
- 收入指标
- 订阅统计
- 连接状态指示器
- 最后更新时间

## 🔧 自定义配置

### 修改更新频率

编辑 `index.html` 第269行：
```javascript
// 改为每2分钟更新
setInterval(fetchData, 2 * 60 * 1000);
```

### 添加更多指标

修改 `api/data.py` 来添加新的数据字段。

## 🆘 故障排除

### 数据显示"Error"
1. 检查Vercel环境变量设置
2. 确认API密钥有效
3. 查看Vercel Function日志

### 页面无法访问
1. 检查Vercel部署状态
2. 清除浏览器缓存
3. 确认DNS解析

## 📞 支持

如有问题，请检查：
1. [DEPLOY.md](DEPLOY.md) - 详细部署指南
2. [CHECKLIST.md](CHECKLIST.md) - 部署检查清单
3. Vercel Dashboard - 查看部署日志

---

**🎉 现在你拥有了一个完全自动化的实时业务仪表板！**

访问部署后的网站即可实时监控 UnlockLand 的业务数据。 