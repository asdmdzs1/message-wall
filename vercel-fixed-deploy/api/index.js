// Vercel Serverless API
const express = require('express');
const cors = require('cors');

// 使用内存数据库
let messages = [];
let nextId = 1;

const app = express();

// 中间件
app.use(cors());
app.use(express.json());

// API路由
app.get('/api/messages', (req, res) => {
    res.json(messages.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)));
});

app.post('/api/messages', (req, res) => {
    const { author, message, color } = req.body;
    
    if (!author || !message) {
        return res.status(400).json({ error: '作者和留言内容不能为空' });
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
        message: '留言发布成功'
    });
});

app.delete('/api/messages/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const index = messages.findIndex(msg => msg.id === id);
    
    if (index === -1) {
        return res.status(404).json({ error: '留言不存在' });
    }
    
    messages.splice(index, 1);
    res.json({ message: '删除成功' });
});

// 导出给Vercel
module.exports = app;