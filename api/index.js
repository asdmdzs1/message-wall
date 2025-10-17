/**
 * Message Wall API - Vercel Serverless Function
 * 
 * This is a serverless API for the Message Wall application.
 * It provides endpoints for creating, reading, and deleting messages.
 * 
 * Note: Uses in-memory storage - data will be lost on serverless function restart.
 * For production use, consider integrating a persistent database like Vercel KV, 
 * Vercel Postgres, or MongoDB Atlas.
 */

const express = require('express');
const cors = require('cors');
const path = require('path');

// In-memory data storage
// WARNING: Data will be lost when the serverless function restarts
let messages = [];
let nextId = 1;

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from public directory (for local development)
app.use(express.static(path.join(__dirname, '..', 'public')));

// Configuration
const MAX_AUTHOR_LENGTH = 20;
const MAX_MESSAGE_LENGTH = 500;

// API路由
app.get('/api/messages', (req, res) => {
    res.json(messages.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)));
});

app.post('/api/messages', (req, res) => {
    const { author, message, color } = req.body;
    
    // Validation
    if (!author || !message) {
        return res.status(400).json({ error: '作者和留言内容不能为空' });
    }
    
    if (author.trim().length === 0 || message.trim().length === 0) {
        return res.status(400).json({ error: '作者和留言内容不能为空' });
    }
    
    if (author.length > MAX_AUTHOR_LENGTH) {
        return res.status(400).json({ error: `昵称不能超过${MAX_AUTHOR_LENGTH}个字符` });
    }
    
    if (message.length > MAX_MESSAGE_LENGTH) {
        return res.status(400).json({ error: `留言内容不能超过${MAX_MESSAGE_LENGTH}个字符` });
    }
    
    const newMessage = {
        id: nextId++,
        author: author.trim(),
        message: message.trim(),
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

// Start server for local development (Vercel will handle this in production)
if (require.main === module) {
    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => {
        console.log(`
🎉 留言墙服务器启动成功！
📍 访问地址: http://localhost:${PORT}
🚀 API 端点: http://localhost:${PORT}/api/messages
        `);
    });
}

// Export for Vercel serverless deployment
module.exports = app;