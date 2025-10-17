/**
 * Validation utilities for the Message Wall application
 */

/**
 * Validates author name
 * @param {string} author - The author name to validate
 * @param {number} maxLength - Maximum length allowed
 * @returns {Object} - { valid: boolean, error: string }
 */
function validateAuthor(author, maxLength = 20) {
    if (!author || typeof author !== 'string') {
        return { valid: false, error: '昵称不能为空' };
    }
    
    if (author.trim().length === 0) {
        return { valid: false, error: '昵称不能为空' };
    }
    
    if (author.length > maxLength) {
        return { valid: false, error: `昵称不能超过${maxLength}个字符` };
    }
    
    return { valid: true };
}

/**
 * Validates message content
 * @param {string} message - The message content to validate
 * @param {number} maxLength - Maximum length allowed
 * @returns {Object} - { valid: boolean, error: string }
 */
function validateMessage(message, maxLength = 500) {
    if (!message || typeof message !== 'string') {
        return { valid: false, error: '留言内容不能为空' };
    }
    
    if (message.trim().length === 0) {
        return { valid: false, error: '留言内容不能为空' };
    }
    
    if (message.length > maxLength) {
        return { valid: false, error: `留言内容不能超过${maxLength}个字符` };
    }
    
    return { valid: true };
}

/**
 * Validates color code
 * @param {string} color - The color code to validate
 * @returns {Object} - { valid: boolean, error: string }
 */
function validateColor(color) {
    if (!color) {
        return { valid: true }; // Color is optional, will use default
    }
    
    const hexColorRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
    if (!hexColorRegex.test(color)) {
        return { valid: false, error: '无效的颜色代码' };
    }
    
    return { valid: true };
}

// Export for Node.js (backend)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateAuthor,
        validateMessage,
        validateColor
    };
}

// Export for browser (frontend)
if (typeof window !== 'undefined') {
    window.Validators = {
        validateAuthor,
        validateMessage,
        validateColor
    };
}

