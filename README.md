# 留言墙网站 - Message Wall

## 项目简介
这是一个简单的留言墙网站，用户可以发布、查看和删除留言。界面美观，支持多种颜色主题。专为 Vercel 无服务器部署优化。

## 功能特点
- ✅ 发布留言（支持昵称、内容、颜色选择）
- ✅ 查看所有留言（按时间倒序）
- ✅ 删除留言
- ✅ 响应式设计（支持手机、平板、电脑）
- ✅ 实时更新
- ✅ 美观的 UI 设计

## 技术栈
- **前端**: HTML5 + CSS3 + JavaScript (原生)
- **后端**: Node.js + Express (Serverless API)
- **存储**: 内存存储（适用于演示和开发）
- **部署**: Vercel

## 项目结构
```
message-wall/
├── api/                   # API 后端
│   └── index.js          # Serverless API 函数
├── public/               # 前端资源
│   ├── index.html        # 主页面
│   ├── script.js         # 前端 JavaScript
│   └── style.css         # 样式文件
├── package.json          # 项目配置
├── vercel.json           # Vercel 部署配置
├── .gitignore           # Git 忽略文件
└── README.md            # 说明文档
```

## 快速开始

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd message-wall
```

### 2. 安装依赖
```bash
npm install
```

### 3. 本地开发
```bash
npm run dev
```

### 4. 访问网站
打开浏览器访问: http://localhost:3000

## API 接口

### 获取所有留言
```
GET /api/messages
```

**响应示例:**
```json
[
  {
    "id": 1,
    "author": "用户昵称",
    "message": "留言内容",
    "color": "#ffeb3b",
    "created_at": "2025-10-17T12:00:00.000Z"
  }
]
```

### 发布新留言
```
POST /api/messages
Content-Type: application/json
```

**请求体:**
```json
{
  "author": "用户昵称",
  "message": "留言内容",
  "color": "#ffeb3b"
}
```

**响应示例:**
```json
{
  "id": 1,
  "message": "留言发布成功"
}
```

### 删除留言
```
DELETE /api/messages/:id
```

**响应示例:**
```json
{
  "message": "删除成功"
}
```

## 部署指南

### Vercel 部署（推荐）

#### 方式一：使用 Vercel CLI
1. 安装 Vercel CLI
```bash
npm install -g vercel
```

2. 登录并部署
```bash
vercel login
vercel
```

#### 方式二：通过 GitHub 集成
1. 将代码推送到 GitHub
2. 访问 [Vercel](https://vercel.com)
3. 导入您的 GitHub 仓库
4. Vercel 会自动检测配置并部署
5. 部署完成后获得访问链接

### 本地开发服务器
```bash
# 开发模式
npm run dev

# 或直接启动
npm start
```

## 重要说明

### 关于数据存储
⚠️ **注意**: 当前版本使用内存存储，这意味着：
- 所有数据在服务器重启后会丢失
- 适合演示、开发和测试用途
- 不适合生产环境的持久化需求

### 生产环境建议
如果需要持久化存储，建议集成以下服务：
- **Vercel KV** (Redis)
- **Vercel Postgres**
- **MongoDB Atlas**
- **Firebase Firestore**
- **Supabase**

## 自定义配置

### 修改颜色主题
在 `public/index.html` 中修改颜色选项:
```html
<option value="#ffeb3b">黄色</option>
<option value="#4caf50">绿色</option>
<!-- 添加更多颜色 -->
```

### 修改字数限制
在 `public/index.html` 中:
```html
<input maxlength="20">        <!-- 昵称限制 -->
<textarea maxlength="500">    <!-- 留言限制 -->
```

在 `api/index.js` 中添加服务器端验证:
```javascript
if (message.length > 500) {
    return res.status(400).json({ error: '留言内容过长' });
}
```

### 修改样式
编辑 `public/style.css` 文件来自定义：
- 背景渐变色
- 卡片样式
- 字体和布局
- 动画效果

## 浏览器支持
- Chrome (推荐)
- Firefox
- Safari
- Edge
- 移动端浏览器

## 开发计划
- [ ] 添加持久化数据库支持
- [ ] 用户认证系统
- [ ] 留言点赞功能
- [ ] 图片上传支持
- [ ] 标签分类功能
- [ ] 搜索和筛选
- [ ] 管理员后台

## 常见问题

### Q: 为什么我的留言消失了？
A: 当前版本使用内存存储，服务器重启后数据会丢失。如需持久化，请集成数据库服务。

### Q: 如何修改端口？
A: 编辑 `api/index.js`，但注意 Vercel 部署时会自动配置端口。

### Q: 可以添加管理员功能吗？
A: 可以！您需要添加身份验证和权限控制逻辑。

### Q: 如何限制恶意留言？
A: 建议添加：
- 内容审核
- 频率限制
- IP 黑名单
- 验证码验证

## 贡献
欢迎提交 Issue 和 Pull Request！

## 许可证
MIT License

## 作者
您的名字

## 致谢
感谢所有贡献者和使用者！
