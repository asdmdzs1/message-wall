// 修改后的server.js - 使用外部数据库
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname)));

// 使用内存数据库（临时解决方案）
let messages = [];
let nextId = 1;

// API路由

// 获取所有留言
app.get('/api/messages', (req, res) => {
    res.json(messages.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)));
});

// 发布新留言
app.post('/api/messages', (req, res) => {
    const { author, message, color } = req.body;
    
    // 验证输入
    if (!author || !message) {
        return res.status(400).json({ error: '作者和留言内容不能为空' });
    }
    
    if (author.length > 20) {
        return res.status(400).json({ error: '昵称不能超过20个字符' });
    }
    
    if (message.length > 500) {
        return res.status(400).json({ error: '留言内容不能超过500个字符' });
    }

    const newMessage = {
        id: nextId++,
        author,
        message,
        color: color || '#ffeb3b',
        created_at: new Date().toISOString()
    };

    messages.push(newMessage);
    res.json({ 
        id: newMessage.id, 
        message: '留言发布成功',
        author,
        message: message,
        color: color || '#ffeb3b'
    });
});

// 删除留言
app.delete('/api/messages/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const index = messages.findIndex(msg => msg.id === id);
    
    if (index === -1) {
        return res.status(404).json({ error: '留言不存在' });
    }
    
    messages.splice(index, 1);
    res.json({ message: '删除成功' });
});

// 获取留言统计
app.get('/api/stats', (req, res) => {
    res.json({ total: messages.length });
});

// 提供静态文件
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// 错误处理中间件
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: '服务器内部错误' });
});

// 404处理
app.use((req, res) => {
    res.status(404).json({ error: '页面不存在' });
});

// 启动服务器
app.listen(PORT, () => {
    console.log(`服务器运行在 http://localhost:${PORT}`);
    console.log('按 Ctrl+C 停止服务器');
});
