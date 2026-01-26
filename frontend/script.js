// API Configuration
const API_BASE_URL = 'https://career-ai-agent-v-1.onrender.com';


// DOM Elements
let chatMessages = document.getElementById('chatMessages');
let userInput = document.getElementById('userInput');
let fileInfo = document.getElementById('fileInfo');
let resumeStatus = document.getElementById('resumeStatus');
let memoryInfo = document.getElementById('memoryInfo');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadMemory();
    updateResumeStatus();
});

// File Upload Handler
document.getElementById('resumeFile').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        fileInfo.innerHTML = `
            <i class="fas fa-file me-1"></i>
            ${file.name} (${formatBytes(file.size)})
        `;
        fileInfo.className = 'mt-2 small text-success';
    }
});

// Send Message Function
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    userInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Send to API
        const formData = new FormData();
        formData.append('user_input', message);
        
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.success) {
            addMessageToChat(data.response, 'ai');
            loadMemory(); // Update memory display
        } else {
            addMessageToChat(`Error: ${data.error}`, 'ai');
        }
    } catch (error) {
        removeTypingIndicator();
        addMessageToChat(`Network error: ${error.message}`, 'ai');
    }
}

// Upload Resume
async function uploadResume() {
    const fileInput = document.getElementById('resumeFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a resume file first.');
        return;
    }
    
    const uploadBtn = document.getElementById('uploadBtn');
    const originalText = uploadBtn.innerHTML;
    uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Uploading...';
    uploadBtn.disabled = true;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/upload-resume`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessageToChat(data.message, 'ai');
            updateResumeStatus();
            loadMemory();
        } else {
            alert(`Upload failed: ${data.error}`);
        }
    } catch (error) {
        alert(`Upload error: ${error.message}`);
    } finally {
        uploadBtn.innerHTML = originalText;
        uploadBtn.disabled = false;
    }
}

// Analyze Match Percentage
async function analyzeMatch() {
    const jd = document.getElementById('jdInput').value;
    if (!jd.trim()) {
        alert('Please enter a job description first.');
        return;
    }
    
    const formData = new FormData();
    formData.append('job_description', jd);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/analyze-match`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessageToChat(data.result, 'ai');
        } else {
            addMessageToChat(`Error: ${data.error}`, 'ai');
        }
    } catch (error) {
        addMessageToChat(`Network error: ${error.message}`, 'ai');
    }
}

// Analyze Skill Gaps
async function analyzeGaps() {
    const jd = document.getElementById('jdInput').value;
    if (!jd.trim()) {
        alert('Please enter a job description first.');
        return;
    }
    
    const formData = new FormData();
    formData.append('job_description', jd);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/skill-gaps`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessageToChat(data.result, 'ai');
        } else {
            addMessageToChat(`Error: ${data.error}`, 'ai');
        }
    } catch (error) {
        addMessageToChat(`Network error: ${error.message}`, 'ai');
    }
}

// Get Alternative Roles
async function getAlternativeRoles() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/alternative-roles`);
        const data = await response.json();
        
        if (data.success) {
            addMessageToChat(data.result, 'ai');
        } else {
            addMessageToChat(`Error: ${data.error}`, 'ai');
        }
    } catch (error) {
        addMessageToChat(`Network error: ${error.message}`, 'ai');
    }
}

// Generate Interview Questions
async function generateQuestions() {
    const company = document.getElementById('companyInput').value;
    const role = document.getElementById('roleInput').value;
    
    if (!company.trim()) {
        alert('Please enter company information.');
        return;
    }
    
    const formData = new FormData();
    formData.append('company', company);
    formData.append('role', role);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/interview-questions`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessageToChat(data.result, 'ai');
        } else {
            addMessageToChat(`Error: ${data.error}`, 'ai');
        }
    } catch (error) {
        addMessageToChat(`Network error: ${error.message}`, 'ai');
    }
}

// Generate Heatmap
async function generateHeatmap() {
    const jd = document.getElementById('jdInput').value;
    if (!jd.trim()) {
        alert('Please enter a job description first.');
        return;
    }
    
    const formData = new FormData();
    formData.append('job_description', jd);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/heatmap`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessageToChat(data.result, 'ai');
        } else {
            addMessageToChat(`Error: ${data.error}`, 'ai');
        }
    } catch (error) {
        addMessageToChat(`Network error: ${error.message}`, 'ai');
    }
}

// Load Memory
async function loadMemory() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/memory`);
        const data = await response.json();
        
        if (data.success) {
            const memory = data.memory.default || data.memory;
            const hasResume = memory.resume_uploaded || false;
            const resumeLength = memory.resume_text ? memory.resume_text.length : 0;
            
            memoryInfo.innerHTML = hasResume ? 
                `<p class="small">
                    <i class="fas fa-check-circle me-1"></i>
                    Resume loaded (${resumeLength} chars)
                </p>` :
                `<p class="small">
                    <i class="fas fa-times-circle me-1"></i>
                    No resume uploaded
                </p>`;
            
            updateResumeStatus();
        }
    } catch (error) {
        console.error('Error loading memory:', error);
    }
}

// Helper Functions
function addMessageToChat(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-bubble ${sender}-message`;
    
    const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-${sender === 'user' ? 'user' : 'robot'}"></i>
        </div>
        <div class="message-content">
            <div class="message-text">${formatMessage(message)}</div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message-bubble ai-message typing-indicator';
    typingDiv.id = 'typingIndicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function formatMessage(text) {
    // Convert markdown-like formatting
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>')
        .replace(/_(.*?)_/g, '<em>$1</em>')
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
}

function updateResumeStatus() {
    const statusDot = document.querySelector('#resumeStatus');
    const memory = memoryInfo.textContent;
    
    if (memory.includes('Resume loaded')) {
        statusDot.className = 'status-dot online';
        statusDot.textContent = '';
    } else {
        statusDot.className = 'status-dot offline';
        statusDot.textContent = '';
    }
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function clearChat() {
    if (confirm('Clear all chat messages?')) {
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <div class="message-bubble ai-message">
                    <div class="message-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content">
                        <div class="message-text">
                            <strong>Chat cleared! 🧹</strong><br>
                            How can I help you with your career today?
                        </div>
                        <div class="message-time">Just now</div>
                    </div>
                </div>
            </div>
        `;
    }
}

function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

function scrollToChat() {
    document.querySelector('.chat-container').scrollIntoView({ behavior: 'smooth' });
    userInput.focus();
}

function scrollToFeatures() {
    document.querySelector('.feature-card').scrollIntoView({ behavior: 'smooth' });
}

function toggleTheme() {
    // Add dark/light theme toggle if needed
    alert('Theme toggle feature coming soon!');
}

function exportChat() {
    // Export chat as text file
    const messages = chatMessages.textContent;
    const blob = new Blob([messages], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'career-ai-chat.txt';
    a.click();
    URL.revokeObjectURL(url);
}
