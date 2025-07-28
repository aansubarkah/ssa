// API Key Storage Module for Browser Environment
class SecureApiStorage {
    constructor() {
        this.storageKey = 'basang_data_api_key';
        this.encryptionKey = 'bd_pdf_converter_2024'; // Simple obfuscation
    }

    // Simple XOR encryption for basic obfuscation
    encrypt(text) {
        if (!text) return '';
        let result = '';
        for (let i = 0; i < text.length; i++) {
            result += String.fromCharCode(text.charCodeAt(i) ^ this.encryptionKey.charCodeAt(i % this.encryptionKey.length));
        }
        return btoa(result);
    }

    decrypt(encrypted) {
        if (!encrypted) return '';
        try {
            const decoded = atob(encrypted);
            let result = '';
            for (let i = 0; i < decoded.length; i++) {
                result += String.fromCharCode(decoded.charCodeAt(i) ^ this.encryptionKey.charCodeAt(i % this.encryptionKey.length));
            }
            return result;
        } catch (e) {
            return '';
        }
    }

    // Save API key to localStorage with encryption
    saveApiKey(apiKey) {
        try {
            const encrypted = this.encrypt(apiKey);
            localStorage.setItem(this.storageKey, encrypted);
            return true;
        } catch (e) {
            console.error('Failed to save API key:', e);
            return false;
        }
    }

    // Load API key from localStorage with decryption
    loadApiKey() {
        try {
            const encrypted = localStorage.getItem(this.storageKey);
            return this.decrypt(encrypted);
        } catch (e) {
            console.error('Failed to load API key:', e);
            return '';
        }
    }

    // Test if API key is valid by making a simple request
    async validateApiKey(apiKey) {
        try {
            const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            return response.ok;
        } catch (e) {
            return false;
        }
    }

    // Clear stored API key
    clearApiKey() {
        try {
            localStorage.removeItem(this.storageKey);
            return true;
        } catch (e) {
            return false;
        }
    }
}