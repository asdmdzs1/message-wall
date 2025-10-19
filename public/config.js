// Configuration file for the Message Wall application
const CONFIG = {
    // API base URL - automatically uses the same domain in production
    API_BASE_URL: '/api',
    
    // UI Configuration
    MAX_AUTHOR_LENGTH: 20,
    MAX_MESSAGE_LENGTH: 500,
    
    // Available colors for messages
    COLORS: [
        { value: '#ffeb3b', name: '黄色' },
        { value: '#4caf50', name: '绿色' },
        { value: '#2196f3', name: '蓝色' },
        { value: '#ff9800', name: '橙色' },
        { value: '#e91e63', name: '粉色' },
        { value: '#9c27b0', name: '紫色' }
    ],
    
    // Notification duration in milliseconds
    NOTIFICATION_DURATION: 3000,
    
    // Animation durations
    ANIMATION: {
        SLIDE_IN: 300,
        SLIDE_OUT: 300
    }
};

// Make config available globally
window.APP_CONFIG = CONFIG;

