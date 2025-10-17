# Vercel部署 - 外部数据库方案

## 推荐的外部数据库服务

### 1. Supabase（推荐）
- **优点**：免费、PostgreSQL、有Web界面
- **缺点**：需要注册账号
- **免费额度**：500MB存储，50,000行数据

### 2. PlanetScale
- **优点**：MySQL、无服务器
- **缺点**：需要信用卡验证
- **免费额度**：1GB存储

### 3. MongoDB Atlas
- **优点**：NoSQL、灵活
- **缺点**：学习成本高
- **免费额度**：512MB存储

## Supabase集成步骤

### 步骤1：创建Supabase项目
1. 访问 https://supabase.com
2. 注册账号
3. 创建新项目
4. 获取数据库连接信息

### 步骤2：修改代码使用Supabase
```javascript
// 安装依赖
npm install @supabase/supabase-js

// 修改server.js使用Supabase
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);
```

### 步骤3：设置环境变量
在Vercel项目设置中添加：
- `SUPABASE_URL`: 您的Supabase项目URL
- `SUPABASE_ANON_KEY`: 您的Supabase匿名密钥

## 当前临时方案

使用内存数据库（server-vercel.js）：
- ✅ 可以立即部署
- ❌ 数据不持久（重启后丢失）
- ✅ 适合演示和测试

## 建议

1. **短期**：使用内存数据库先部署上线
2. **长期**：集成Supabase实现数据持久化
3. **备选**：考虑使用其他平台（如Railway、Render）
