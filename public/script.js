// 前端JavaScript代码
class MessageWall {
    constructor() {
        this.apiUrl = '/api';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadMessages();
    }

    bindEvents() {
        const form = document.getElementById('messageForm');
        form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const messageData = {
            author: formData.get('author'),
            message: formData.get('message'),
            color: formData.get('color')
        };

        try {
            const response = await fetch(`${this.apiUrl}/messages`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(messageData)
            });

            if (response.ok) {
                e.target.reset();
                this.loadMessages();
                this.showNotification('留言发布成功！', 'success');
            } else {
                throw new Error('发布失败');
            }
        } catch (error) {
            this.showNotification('发布失败，请重试', 'error');
            console.error('Error:', error);
        }
    }

    async loadMessages() {
        const container = document.getElementById('messagesContainer');
        container.innerHTML = '<div class="loading">加载中...</div>';

        try {
            const response = await fetch(`${this.apiUrl}/messages`);
            const messages = await response.json();

            if (messages.length === 0) {
                container.innerHTML = '<div class="no-messages">还没有留言，快来发布第一条吧！</div>';
                return;
            }

            container.innerHTML = '';
            messages.forEach(message => {
                const messageElement = this.createMessageElement(message);
                container.appendChild(messageElement);
            });
        } catch (error) {
            container.innerHTML = '<div class="error">加载留言失败，请刷新页面重试</div>';
            console.error('Error:', error);
        }
    }

    createMessageElement(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message-card';
        messageDiv.style.backgroundColor = message.color + '20';
        messageDiv.style.borderLeft = `4px solid ${message.color}`;

        const time = new Date(message.created_at).toLocaleString('zh-CN');
        
        messageDiv.innerHTML = `
            <button class="delete-btn" onclick="messageWall.deleteMessage(${message.id})">×</button>
            <div class="message-author">${this.escapeHtml(message.author)}</div>
            <div class="message-content">${this.escapeHtml(message.message)}</div>
            <div class="message-time">${time}</div>
        `;

        return messageDiv;
    }

    async deleteMessage(id) {
        if (!confirm('确定要删除这条留言吗？')) {
            return;
        }

        try {
            const response = await fetch(`${this.apiUrl}/messages/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.loadMessages();
                this.showNotification('留言已删除', 'success');
            } else {
                throw new Error('删除失败');
            }
        } catch (error) {
            this.showNotification('删除失败，请重试', 'error');
            console.error('Error:', error);
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            z-index: 1000;
            animation: slideInRight 0.3s ease;
            background: ${type === 'success' ? '#4caf50' : '#f44336'};
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// 添加通知动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// 初始化应用
const messageWall = new MessageWall();
