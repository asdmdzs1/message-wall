# 留言墙网站 - 使用说明

## 项目简介
这是一个简单的留言墙网站，用户可以发布、查看和删除留言。界面美观，支持多种颜色主题。

## 功能特点
- ✅ 发布留言（支持昵称、内容、颜色选择）
- ✅ 查看所有留言（按时间倒序）
- ✅ 删除留言
- ✅ 响应式设计（支持手机、平板、电脑）
- ✅ 实时更新
- ✅ 数据持久化存储

## 技术栈
- **前端**: HTML5 + CSS3 + JavaScript (原生)
- **后端**: Node.js + Express
- **数据库**: SQLite
- **部署**: 支持多种平台

## 快速开始

### 1. 安装依赖
```bash
npm install
```

### 2. 启动服务器
```bash
npm start
```

### 3. 访问网站
打开浏览器访问: http://localhost:3000

## 开发模式
```bash
npm run dev
```
使用 nodemon 自动重启服务器

## 项目结构
```
message-wall/
├── index.html          # 主页面
├── style.css           # 样式文件
├── script.js           # 前端JavaScript
├── server.js           # 后端服务器
├── package.json        # 项目配置
├── messages.db         # SQLite数据库（自动创建）
└── README.md           # 说明文档
```

## API接口

### 获取所有留言
```
GET /api/messages
```

### 发布新留言
```
POST /api/messages
Content-Type: application/json

{
  "author": "用户昵称",
  "message": "留言内容",
  "color": "#ffeb3b"
}
```

### 删除留言
```
DELETE /api/messages/:id
```

### 获取统计信息
```
GET /api/stats
```

## 部署指南

### 1. Vercel 部署
1. 将代码推送到 GitHub
2. 在 Vercel 导入项目
3. 设置环境变量（如需要）
4. 部署完成

### 2. Heroku 部署
1. 创建 Heroku 应用
2. 连接 GitHub 仓库
3. 启用自动部署
4. 部署完成

### 3. 本地服务器部署
1. 安装 PM2: `npm install -g pm2`
2. 启动应用: `pm2 start server.js --name message-wall`
3. 设置开机自启: `pm2 startup`

## 自定义配置

### 修改端口
在 `server.js` 中修改:
```javascript
const PORT = process.env.PORT || 3000;
```

### 修改数据库
在 `server.js` 中修改数据库文件路径:
```javascript
const db = new sqlite3.Database('./messages.db');
```

### 添加新功能
1. 修改数据库表结构
2. 更新 API 接口
3. 修改前端界面
4. 更新样式

## 常见问题

### Q: 如何备份数据？
A: 复制 `messages.db` 文件即可

### Q: 如何清空所有留言？
A: 删除 `messages.db` 文件，重启服务器会自动创建新数据库

### Q: 如何修改留言字数限制？
A: 在 `server.js` 和 `script.js` 中修改验证逻辑

## 许可证
MIT License

## 贡献
欢迎提交 Issue 和 Pull Request！