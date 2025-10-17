/**
 * Application Constants
 */

// Validation limits
const VALIDATION = {
    MAX_AUTHOR_LENGTH: 20,
    MAX_MESSAGE_LENGTH: 500,
    MIN_AUTHOR_LENGTH: 1,
    MIN_MESSAGE_LENGTH: 1
};

// Available message colors
const COLORS = {
    YELLOW: '#ffeb3b',
    GREEN: '#4caf50',
    BLUE: '#2196f3',
    ORANGE: '#ff9800',
    PINK: '#e91e63',
    PURPLE: '#9c27b0'
};

// Default values
const DEFAULTS = {
    COLOR: COLORS.YELLOW,
    NOTIFICATION_DURATION: 3000
};

// API endpoints
const API_ENDPOINTS = {
    MESSAGES: '/api/messages',
    MESSAGE_BY_ID: (id) => `/api/messages/${id}`
};

// HTTP status codes
const HTTP_STATUS = {
    OK: 200,
    CREATED: 201,
    BAD_REQUEST: 400,
    NOT_FOUND: 404,
    INTERNAL_SERVER_ERROR: 500
};

// Export for Node.js (backend)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        VALIDATION,
        COLORS,
        DEFAULTS,
        API_ENDPOINTS,
        HTTP_STATUS
    };
}

// Export for browser (frontend)
if (typeof window !== 'undefined') {
    window.Constants = {
        VALIDATION,
        COLORS,
        DEFAULTS,
        API_ENDPOINTS,
        HTTP_STATUS
    };
}

